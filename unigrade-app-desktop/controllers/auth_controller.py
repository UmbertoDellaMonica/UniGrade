from configuration.database_configuration import get_connection
from utils import hash_password


def login(matricola, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM students WHERE matricola=? AND password=?",
        (matricola, hash_password(password)),
    )
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None


def register(nome, cognome, corso, matricola, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO students (nome,cognome,corso,matricola,password) VALUES (?,?,?,?,?)",
            (nome, cognome, corso, matricola, hash_password(password)),
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False
