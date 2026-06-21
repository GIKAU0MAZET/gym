from database import get_connection

def get_all_abonement_types():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_типа_абонента, название, стоимость, срок_дней FROM типы_абонементов ORDER BY название")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_client_abonements():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            а.id_абонемента,
            к.фамилия || ' ' || к.имя AS клиент,
            т.название AS тип,
            т.стоимость,
            а.дата_начала,
            а.дата_окончания,
            а.номер_абонемента
        FROM абонементы_клиентов а
        JOIN клиенты к ON к.id_клиента = а.id_клиента
        JOIN типы_абонементов т ON т.id_типа_абонента = а.id_типа_абонента
        ORDER BY а.id_абонемента DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_abonement_by_id(abo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_абонемента, id_клиента, id_типа_абонента, дата_начала, дата_окончания, номер_абонемента
        FROM абонементы_клиентов WHERE id_абонемента = %s
    """, (abo_id,))
    row = cur.fetchone()
    conn.close()
    return row

def add_client_abonement(client_id, type_id, start_date, end_date, number, employee_id, request_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO абонементы_клиентов (id_клиента, id_типа_абонента, дата_начала, дата_окончания, номер_абонемента)
        VALUES (%s, %s, %s, %s, %s)
    """, (client_id, type_id, start_date, end_date, number))
    # Записываем продажу
    cur.execute("""
        INSERT INTO продажа_абонемента (id_сотрудника, id_заявки, дата_продажи)
        VALUES (%s, %s, CURRENT_DATE)
    """, (employee_id, request_id))
    # Закрываем заявку
    if request_id:
        cur.execute("UPDATE заявки SET статус='Выполнена' WHERE id_заявки=%s", (request_id,))
    conn.commit()
    conn.close()

def update_client_abonement(abo_id, client_id, type_id, start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE абонементы_клиентов
        SET id_клиента=%s, id_типа_абонента=%s, дата_начала=%s, дата_окончания=%s
        WHERE id_абонемента=%s
    """, (client_id, type_id, start_date, end_date, abo_id))
    conn.commit()
    conn.close()
