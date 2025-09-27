from configuration.database_configuration import get_connection
import sqlite3


def get_exams(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nome, voto, cfu FROM exams WHERE student_id=?", (student_id,)
    )
    exams = cur.fetchall()
    conn.close()
    return exams


def add_exam(student_id, nome, voto=None, cfu=0):
    """
    Aggiunge un esame al database.
    Restituisce:
        True -> se l'inserimento è avvenuto con successo
        False -> se l'esame esiste già per questo studente
    """

    conn = get_connection()
    cur = conn.cursor()

    # Controllo preventivo duplicato
    cur.execute(
        "SELECT id FROM exams WHERE student_id=? AND nome=?", (student_id, nome)
    )
    if cur.fetchone():
        conn.close()
        return False  # esame già presente

    try:
        cur.execute(
            "INSERT INTO exams (student_id, nome, voto, cfu) VALUES (?, ?, ?, ?)",
            (student_id, nome, voto, cfu),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # caso rarissimo se UNIQUE vincolo su DB
        conn.close()
        return False
    finally:
        conn.close()

    return True


def update_exam(exam_id, nome, voto, cfu):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE exams SET nome=?, voto=?, cfu=? WHERE id=?", (nome, voto, cfu, exam_id)
    )
    conn.commit()
    conn.close()


def remove_exam(exam_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM exams WHERE id=?", (exam_id,))
    conn.commit()
    conn.close()
