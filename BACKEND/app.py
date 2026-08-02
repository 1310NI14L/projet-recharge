import smtplib
import ssl
import pymysql
from email.message import EmailMessage
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
# Import de la fonction de connexion et des identifiants Gmail depuis database.py
from database import get_db_connection, GMAIL_USER, GMAIL_PASSWORD

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)


# --- ROUTES PAGES HTML ---

@app.route('/')
def home():
    return {"status": "online", "message": "API Projet Recharge operational"}, 200

@app.route('/index.html')
def index():
    return send_from_directory('../frontend', 'index.html')


@app.route('/controle.html')
def controle_page():
    return send_from_directory('../frontend', 'controle.html')


@app.route('/statut.html')
def statut_page():
    return send_from_directory('../frontend', 'statut.html')


@app.route('/produit.html')
def produit_page():
    return send_from_directory('../frontend', 'produit.html')


# Route pour servir les assets (CSS, JS, images)
@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('../frontend/assets', path)


# --- ROUTES API ---

@app.route('/api/tickets', methods=['POST'])
def submit_ticket():
    try:
        data = request.get_json()
        type_carte = data.get('type_carte')
        montant = data.get('montant')
        code_ticket = data.get('code_ticket', '').strip()
        user_email = data.get('user_email', '').strip() or None

        if not type_carte or not montant or not code_ticket:
            return jsonify({'error': 'Tous les champs obligatoires doivent être remplis.'}), 400

        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO tickets (type_carte, montant, code_ticket, user_email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (type_carte, float(montant), code_ticket, user_email))
            ticket_id = cursor.lastrowid

        conn.commit()
        conn.close()

        # Envoi de notification e-mail au propriétaire
        try:
            send_ticket_notification(
                ticket_id=ticket_id,
                type_carte=type_carte,
                montant=montant,
                code_ticket=code_ticket,
                user_email=user_email
            )
        except Exception as email_error:
            print(f"Erreur envoi e-mail : {email_error}")

        return jsonify({
            'message': 'Ticket soumis avec succès !',
            'ticket_id': ticket_id,
        }), 201

    except pymysql.MySQLError as e:
        return jsonify({'error': f'Erreur de base de données : {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500


def send_ticket_notification(ticket_id, type_carte, montant, code_ticket, user_email):
    if not GMAIL_USER or not GMAIL_PASSWORD:
        raise RuntimeError('Les identifiants Gmail ne sont pas configurés.')

    subject = f"Nouveau ticket soumis - {type_carte}"
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background:#f2f4f8; color:#0f172a; padding: 20px;">
        <div style="max-width: 600px; margin:auto; background:#ffffff; border-radius:16px; box-shadow:0 16px 40px rgba(15,23,42,.08); overflow:hidden;">
          <div style="background:#0d6efd; color:#fff; padding:24px 30px; text-align:center;">
            <h1 style="font-size:1.6rem; margin:0;">Nouveau ticket soumis</h1>
            <p style="margin:8px 0 0; font-size:0.95rem; opacity:.85;">Jacques Recharge - Notification instantanée</p>
          </div>
          <div style="padding:28px 30px;">
            <p style="font-size:1rem; margin:0 0 18px;">Un utilisateur a soumis un nouveau ticket. Retrouvez ci-dessous les détails :</p>
            <table style="width:100%; border-collapse:collapse; font-size:0.95rem;">
              <tr>
                <td style="padding:10px 0; font-weight:600; width:140px;">ID</td>
                <td style="padding:10px 0;">{ticket_id}</td>
              </tr>
              <tr style="background:#f8fafc;">
                <td style="padding:10px 0; font-weight:600;">Type</td>
                <td style="padding:10px 0;">{type_carte}</td>
              </tr>
              <tr>
                <td style="padding:10px 0; font-weight:600;">Montant</td>
                <td style="padding:10px 0;">{montant} €</td>
              </tr>
              <tr style="background:#f8fafc;">
                <td style="padding:10px 0; font-weight:600;">Code</td>
                <td style="padding:10px 0;">{code_ticket}</td>
              </tr>
              <tr>
                <td style="padding:10px 0; font-weight:600;">E-mail utilisateur</td>
                <td style="padding:10px 0;">{user_email or 'Non renseigné'}</td>
              </tr>
              <tr style="background:#f8fafc;">
                <td style="padding:10px 0; font-weight:600;">Statut</td>
                <td style="padding:10px 0;">EN_ATTENTE</td>
              </tr>
            </table>
            <p style="font-size:0.9rem; color:#475569; margin:24px 0 0;">Connectez-vous à l'administration pour gérer ce ticket et vérifier son avancement.</p>
          </div>
          <div style="background:#f8fafc; padding:18px 30px; font-size:0.85rem; color:#64748b; text-align:center;">
            © 2026 Jacques Recharge
          </div>
        </div>
      </body>
    </html>
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"Jacques Recharge <{GMAIL_USER}>"
    msg['To'] = GMAIL_USER
    msg.set_content('Un nouveau ticket a été soumis. Ouvrez l’e-mail en HTML pour voir les détails.')
    msg.add_alternative(html_body, subtype='html')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)


@app.route('/api/tickets/status', methods=['GET'])
def check_status():
    # Nettoyage de la saisie utilisateur
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'error': 'Veuillez fournir un code de ticket ou une adresse e-mail.'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Recherche flexible et insensible aux espaces/casse
            sql = """
                SELECT id, type_carte, montant, statut, created_at 
                FROM tickets 
                WHERE LOWER(TRIM(code_ticket)) LIKE LOWER(%s) 
                   OR LOWER(TRIM(user_email)) LIKE LOWER(%s)
                ORDER BY created_at DESC
            """
            search_param = f"%{query}%"
            cursor.execute(sql, (search_param, search_param))
            results = cursor.fetchall()

        conn.close()

        for row in results:
            if row.get('created_at'):
                row['created_at'] = str(row['created_at'])

        return jsonify(results), 200

    except pymysql.MySQLError as e:
        print(f"Erreur MySQL : {str(e)}")
        return jsonify({'error': f'Erreur de base de données : {str(e)}'}), 500
    except Exception as e:
        print(f"Erreur Python : {str(e)}")
        return jsonify({'error': f'Erreur serveur : {str(e)}'}), 500

if __name__ == '__main__':
    print('Serveur Flask demarre sur http://127.0.0.1:5000')
    app.run(port=5000)