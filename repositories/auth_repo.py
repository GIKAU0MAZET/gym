from database import get_connection

def get_user_by_login(login):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            п.пользователь_id,
            п.логин,
            п.пароль_hash,
            с.id_сотрудника,
            с.должность,
            с.фамилия || ' ' || с.имя AS fio
        FROM пользователи п
        JOIN сотрудники с ON п.сотрудник_id = с.id_сотрудника
        WHERE п.логин = %s
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row
