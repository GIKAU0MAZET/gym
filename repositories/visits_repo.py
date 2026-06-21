from database import get_connection


def get_all_visits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            п.id_посещения,
            к.фамилия || ' ' || к.имя AS клиент,
            п.дата_время,
            п.статус
        FROM посещения п
        JOIN клиенты к ON к.id_клиента = п.id_клиента
        ORDER BY п.дата_время DESC
        LIMIT 100
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def add_visit(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO посещения (id_клиента, дата_время, статус)
        VALUES (%s, NOW(), 'Вход')
    """, (client_id,))
    conn.commit()
    conn.close()
