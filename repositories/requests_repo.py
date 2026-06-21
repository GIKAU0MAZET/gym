from database import get_connection

def get_all_requests():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            з.id_заявки,
            к.фамилия || ' ' || к.имя AS клиент,
            т.название AS тип_абонемента,
            с.фамилия || ' ' || с.имя AS сотрудник,
            з.дата_заявки,
            з.статус
        FROM заявки з
        JOIN клиенты к ON к.id_клиента = з.id_клиента
        JOIN типы_абонементов т ON т.id_типа_абонента = з.id_типа_абонента
        JOIN сотрудники с ON с.id_сотрудника = з.id_сотрудника
        ORDER BY з.id_заявки DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_request_by_id(req_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_заявки, id_клиента, id_типа_абонента, id_сотрудника, дата_заявки, статус
        FROM заявки WHERE id_заявки = %s
    """, (req_id,))
    row = cur.fetchone()
    conn.close()
    return row

def add_request(client_id, type_id, employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO заявки (id_клиента, id_типа_абонента, id_сотрудника, дата_заявки, статус)
        VALUES (%s, %s, %s, CURRENT_DATE, 'Новая')
    """, (client_id, type_id, employee_id))
    conn.commit()
    conn.close()

def update_request(req_id, client_id, type_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE заявки SET id_клиента=%s, id_типа_абонента=%s, статус=%s
        WHERE id_заявки=%s
    """, (client_id, type_id, status, req_id))
    conn.commit()
    conn.close()
