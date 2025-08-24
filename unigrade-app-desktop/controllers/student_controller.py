from database import get_connection
from utils import hash_password
# Funzione helper per hash della password



def get_students():
    """Restituisce tutti gli studenti presenti nel DB"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, matricola, nome, cognome, corso FROM students")
    students = cur.fetchall()
    conn.close()
    return students


def get_student(student_id):
    """Restituisce uno studente per id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )
    student = cur.fetchone()
    conn.close()
    return student



def get_student_by_matricola(matricola_id):
    """Restituisce uno studente per id"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, matricola, nome, cognome, corso, password FROM students WHERE matricola=?",
        (matricola_id,)
    )
    student = cur.fetchone()
    conn.close()
    return student


def add_student(matricola, nome, cognome, corso, password):
    """Aggiunge un nuovo studente al DB"""
    conn = get_connection()
    cur = conn.cursor()
    pw_hash = hash_password(password)
    cur.execute(
        "INSERT INTO students (matricola, nome, cognome, corso, password) VALUES (?,?,?,?,?)",
        (matricola, nome, cognome, corso, pw_hash)
    )
    conn.commit()
    conn.close()


def update_student(student_id, nome=None, cognome=None, corso=None, password=None):
    """Aggiorna i dati di uno studente"""
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []

    if nome is not None:
        fields.append("nome=?")
        values.append(nome)
    if cognome is not None:
        fields.append("cognome=?")
        values.append(cognome)
    if corso is not None:
        fields.append("corso=?")
        values.append(corso)
    if password is not None:
        fields.append("password=?")
        values.append(hash_password(password))

    if not fields:
        conn.close()
        return  # niente da aggiornare

    values.append(student_id)
    sql = f"UPDATE students SET {', '.join(fields)} WHERE id=?"
    cur.execute(sql, tuple(values))
    conn.commit()
    conn.close()


def remove_student(student_id):
    """Rimuove uno studente dal DB"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
