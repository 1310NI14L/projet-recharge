import pymysql

# Connexion à Aiven MySQL
connection = pymysql.connect(
    host='mysql-jr1e48e891-jacquesrecharge16-d706.c.aivencloud.com',
    port=13980,
    user='avnadmin',
    password='AVNS_uHJj7lJelC6UYhqsc3-',
    database='defaultdb',
    ssl={'ssl': {}}
)

sql_script = """
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_carte VARCHAR(50) NOT NULL,
    montant DECIMAL(10, 2) NOT NULL,
    code_ticket TEXT NOT NULL,
    user_email VARCHAR(255),
    date_soumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

try:
    with connection.cursor() as cursor:
        cursor.execute(sql_script)
    connection.commit()
    print("Table 'tickets' créée avec succès sur Aiven !")
finally:
    connection.close()