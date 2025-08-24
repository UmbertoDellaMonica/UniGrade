import sqlite3

DB_NAME = "unigrade.db"

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cognome TEXT,
        corso TEXT,
        matricola TEXT UNIQUE,
        password TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        nome TEXT,
        voto INTEGER,
        cfu INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)
    conn.commit()
    conn.close()

def get_connection():
    """Restituisce una connessione SQLite con row_factory per ottenere dizionari"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
