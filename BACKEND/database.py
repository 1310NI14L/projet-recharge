import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

# 1. On charge les variables cachées dans le .env
load_dotenv()

# Récupération des données
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

# 2. On crée le dictionnaire de connexion à partir des variables
def get_db_connection():
    
    # Contexte SSL obligatoire pour Aiven
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'mysql-jr1e48e891-jacquesrecharge16-d706.c.aivencloud.com'),
        user=os.getenv('DB_USER', 'avnadmin'),
        password=os.getenv('DB_PASSWORD', 'AVNS_uHJj7IJeIC6UYhqsc3-'),
        database=os.getenv('DB_NAME', 'defaultdb'),
        port=int(os.getenv('DB_PORT', 13980)),
        ssl={'ssl': {}},  # Obligatoire pour la connexion SSL requise par Aiven
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4',
  )



