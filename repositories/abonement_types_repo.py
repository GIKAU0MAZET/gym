from database import get_connection


def get_all_types():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_типа_абонента, название, стоимость, срок_дней
        FROM типы_абонементов
        ORDER BY название
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_type_by_id(type_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_типа_абонента, название, стоимость, срок_дней
        FROM типы_абонементов WHERE id_типа_абонента = %s
    """, (type_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_type(name, cost, days):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO типы_абонементов (название, стоимость, срок_дней)
        VALUES (%s, %s, %s)
    """, (name, cost, days))
    conn.commit()
    conn.close()


def update_type(type_id, name, cost, days):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE типы_абонементов
        SET название=%s, стоимость=%s, срок_дней=%s
        WHERE id_типа_абонента=%s
    """, (name, cost, days, type_id))
    conn.commit()
    conn.close()
