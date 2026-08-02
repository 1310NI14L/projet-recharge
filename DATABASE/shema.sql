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


