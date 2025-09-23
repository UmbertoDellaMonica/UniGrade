from configuration.database_configuration import get_connection


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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO exams (student_id,nome,voto,cfu) VALUES (?,?,?,?)",
        (student_id, nome, voto, cfu),
    )
    conn.commit()
    conn.close()


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
