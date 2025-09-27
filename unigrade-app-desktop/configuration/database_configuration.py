import sqlite3
import hashlib
from configuration.unigrade_configuration import DB_NAME


# Hash Password - UniGrade Application
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Creazione tabella students con avatar_path
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cognome TEXT,
        corso TEXT,
        matricola TEXT UNIQUE,
        password TEXT,
        avatar_path TEXT
    )
    """
    )

    # Creazione tabella exams
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        nome TEXT UNIQUE,
        voto TEXT,
        cfu INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """
    )

    conn.commit()
    conn.close()


def get_connection():
    """Restituisce una connessione SQLite con row_factory per ottenere dizionari"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
