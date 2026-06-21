from database import get_connection

def get_all_trainings():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            т.id_тренировки,
            т.название_тренировки,
            с.фамилия || ' ' || с.имя AS тренер,
            т.дата_время,
            т.максимальное_участников,
            COUNT(кт.id_клиента) AS записано
        FROM тренировки т
        JOIN сотрудники с ON с.id_сотрудника = т.id_сотрудника
        LEFT JOIN клиенты_тренировки кт ON кт.id_тренировки = т.id_тренировки
        GROUP BY т.id_тренировки, с.фамилия, с.имя
        ORDER BY т.дата_время DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_training_by_id(tr_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_тренировки, id_сотрудника, id_зала, дата_время, название_тренировки, максимальное_участников
        FROM тренировки WHERE id_тренировки=%s
    """, (tr_id,))
    row = cur.fetchone()
    conn.close()
    return row

def add_training(employee_id, hall_id, datetime_val, name, max_participants):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO тренировки (id_сотрудника, id_зала, дата_время, название_тренировки, максимальное_участников)
        VALUES (%s, %s, %s, %s, %s)
    """, (employee_id, hall_id, datetime_val, name, max_participants))
    conn.commit()
    conn.close()

def update_training(tr_id, employee_id, datetime_val, name, max_participants):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE тренировки SET id_сотрудника=%s, дата_время=%s, название_тренировки=%s, максимальное_участников=%s
        WHERE id_тренировки=%s
    """, (employee_id, datetime_val, name, max_participants, tr_id))
    conn.commit()
    conn.close()

def get_training_clients(tr_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT к.id_клиента, к.фамилия, к.имя, кт.дата_записи, кт.отметка_посещения
        FROM клиенты_тренировки кт
        JOIN клиенты к ON к.id_клиента = кт.id_клиента
        WHERE кт.id_тренировки = %s
        ORDER BY к.фамилия
    """, (tr_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def enroll_client(tr_id, client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO клиенты_тренировки (id_клиента, id_тренировки, дата_записи, отметка_посещения)
        VALUES (%s, %s, CURRENT_DATE, FALSE)
        ON CONFLICT DO NOTHING
    """, (client_id, tr_id))
    conn.commit()
    conn.close()

def mark_attendance(tr_id, client_id, attended):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE клиенты_тренировки SET отметка_посещения=%s
        WHERE id_тренировки=%s AND id_клиента=%s
    """, (attended, tr_id, client_id))
    conn.commit()
    conn.close()
