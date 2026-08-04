# 💳 Plateforme Web de Recharge & Contrôle de Tickets Prépayés

Application web full-stack permettant de gérer la soumission, le suivi et la validation de tickets et de coupons prépayés en temps réel.

---

## 🧩 Présentation de l'Architecture

Le projet s'appuie sur une séparation claire entre le client (frontend statique) et l'API (backend), garantissant un déploiement indépendant et une maintenance facilitée :

- **Frontend** : Interface utilisateur réactive développée en HTML5, CSS3, JavaScript (ES6+) et Bootstrap.
- **Backend** : API RESTful développée avec Flask (Python) gérant la logique métier, l'accès aux données et l'envoi d'e-mails de notification.
- **Base de données** : Relationnelle (MySQL) stockant les demandes de tickets, leurs détails et leur état d'avancement.

---

## 📁 Structure du Projet

projet-recharge/
│
├── backend/
│   ├── app.py              # Application Flask & définition des routes API
│   ├── database.py         # Gestionnaire de connexion MySQL & variables d'environnement
│   ├── .env.example        # Modèle de configuration des secrets local
│   ├── .gitignore          # Fichiers et dossiers ignorés par Git pour le backend
│   └── requirements.txt    # Dépendances Python (Flask, PyMySQL, Gunicorn, etc.)
│
├── database/
│   └── shema.sql           # Script SQL d'initialisation de la base et de la table
│
├── frontend/
│   ├── index.html          # Page d'accueil & catalogue des cartes / coupons
│   ├── produit.html        # Page produit dynamique selon l'opérateur sélectionné
│   ├── controle.html       # Formulaire de soumission et de contrôle du ticket
│   ├── statut.html         # Visualisation des résultats de recherche de ticket
│   └── assets/
│       ├── bootstrap.bundle.min.js
│       ├── bootstrap.min.css
│       ├── main.js         # Logique d'interaction JS & requêtes Fetch vers l'API
│       ├── style.css       # Feuilles de styles personnalisées
│       └── image/          # Ressources visuelles et logos des opérateurs
│
├── README.md               # Documentation globale du projet
└── venv/                   # Environnement virtuel Python (exclu du suivi Git)

---

## ⚙️ Configuration de l'Environnement

1. Accède au dossier backend/ et duplique le fichier exemple :
   cd backend
   cp .env.example .env

2. Ajuste les variables dans le fichier .env selon ta configuration :

# Configuration de la base de données
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=recharge_db

# Configuration du service E-mail (Gmail SMTP / App Password)
GMAIL_USER=danielahouansou16@gmail.com
GMAIL_PASSWORD="votre_mot_de_passe_application"

> ⚠️ **Sécurité :** Ne commite jamais le fichier backend/.env sur un dépôt public.

---

## 🧪 Installation & Exécution en Local

### 1. Préparer l'environnement Python

Depuis la racine du projet, crée et active un environnement virtuel, puis installe les dépendances :

# Activation (sur Windows CMD / PowerShell)
venv\Scripts\activate

# Activation (sur Linux / macOS)
source venv/bin/activate

# Installation des dépendances
cd backend
python -m pip install -r requirements.txt

### 2. Démarrer le Serveur Backend Flask

cd backend
python app.py

Le serveur local démarrera sur http://127.0.0.1:5000.

---

## 🗄️ Initialisation de la Base de Données

Exécute le script SQL suivant dans ton SGBD (MySQL / phpMyAdmin) pour initialiser la base de données et la structure des tables :

CREATE DATABASE IF NOT EXISTS recharge_db;
USE recharge_db;

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type_carte VARCHAR(50) NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    code_ticket VARCHAR(255) NOT NULL,
    user_email VARCHAR(150) NULL,
    statut VARCHAR(20) NOT NULL DEFAULT 'EN_ATTENTE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code_ticket (code_ticket),
    INDEX idx_user_email (user_email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

---

## 🚢 Guide de Déploiement Production

### Frontend (ex: Netlify / Vercel)
- **Root directory** : frontend
- **Build command** : (laisser vide pour des pages statiques)
- **Publish directory** : . (ou frontend)

### Backend (ex: Render / Railway / Heroku)
- **Root directory** : backend (ou laisser la racine avec commande ciblée)
- **Commande de démarrage (WSGI)** : gunicorn backend.app:app (ou gunicorn app:app si le root directory du service est configuré sur backend)
- **Variables d'environnement** : Configure DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, GMAIL_USER, et GMAIL_PASSWORD directement dans le panneau de ton hébergeur.