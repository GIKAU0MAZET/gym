from database import get_connection

def get_all_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_клиента, фамилия, имя, отчество, телефон, email, дата_регистрации
        FROM клиенты
        ORDER BY фамилия
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_client_by_id(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_клиента, фамилия, имя, отчество, телефон, email, дата_регистрации
        FROM клиенты WHERE id_клиента = %s
    """, (client_id,))
    row = cur.fetchone()
    conn.close()
    return row

def add_client(last_name, first_name, middle_name, phone, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO клиенты (фамилия, имя, отчество, телефон, email, дата_регистрации)
        VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
    """, (last_name, first_name, middle_name, phone, email))
    conn.commit()
    conn.close()

def update_client(client_id, last_name, first_name, middle_name, phone, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE клиенты SET фамилия=%s, имя=%s, отчество=%s, телефон=%s, email=%s
        WHERE id_клиента=%s
    """, (last_name, first_name, middle_name, phone, email, client_id))
    conn.commit()
    conn.close()
