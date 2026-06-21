from database import get_connection

def get_gym_info():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT название_зала, электронная_почта, контактный_телефон,
               юридический_адрес, фактический_адрес,
               фамилия_директора || ' ' || имя_директора || ' ' || отчество_директора AS директор
        FROM тренажерный_зал LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()
    return row

def get_all_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_сотрудника, фамилия, имя, отчество, должность, телефон, email, дата_приема
        FROM сотрудники ORDER BY фамилия
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_employee_by_id(emp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_сотрудника, фамилия, имя, отчество, должность, телефон, email, дата_приема
        FROM сотрудники WHERE id_сотрудника=%s
    """, (emp_id,))
    row = cur.fetchone()
    conn.close()
    return row

def add_employee(last_name, first_name, middle_name, position, phone, email, hire_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO сотрудники (фамилия, имя, отчество, должность, телефон, email, дата_приема)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (last_name, first_name, middle_name, position, phone, email, hire_date))
    conn.commit()
    conn.close()

def update_employee(emp_id, last_name, first_name, middle_name, position, phone, email, hire_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE сотрудники SET фамилия=%s, имя=%s, отчество=%s, должность=%s,
               телефон=%s, email=%s, дата_приема=%s
        WHERE id_сотрудника=%s
    """, (last_name, first_name, middle_name, position, phone, email, hire_date, emp_id))
    conn.commit()
    conn.close()

def get_abonement_sales_report(date_from, date_to):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT т.название, COUNT(*) AS продаж, SUM(т.стоимость) AS выручка
        FROM продажа_абонемента п
        JOIN заявки з ON з.id_заявки = п.id_заявки
        JOIN типы_абонементов т ON т.id_типа_абонента = з.id_типа_абонента
        WHERE п.дата_продажи BETWEEN %s AND %s
        GROUP BY т.название
        ORDER BY выручка DESC
    """, (date_from, date_to))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_active_abonements_report():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT к.фамилия || ' ' || к.имя AS клиент,
               т.название AS тип,
               а.дата_начала, а.дата_окончания, а.номер_абонемента
        FROM абонементы_клиентов а
        JOIN клиенты к ON к.id_клиента = а.id_клиента
        JOIN типы_абонементов т ON т.id_типа_абонента = а.id_типа_абонента
        WHERE а.дата_окончания >= CURRENT_DATE
        ORDER BY а.дата_окончания
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_trainer_trainings_report():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT с.фамилия || ' ' || с.имя AS тренер,
               COUNT(т.id_тренировки) AS тренировок,
               COUNT(кт.id_клиента) AS клиентов_всего
        FROM сотрудники с
        LEFT JOIN тренировки т ON т.id_сотрудника = с.id_сотрудника
        LEFT JOIN клиенты_тренировки кт ON кт.id_тренировки = т.id_тренировки
        WHERE с.должность = 'Тренер'
        GROUP BY с.id_сотрудника, с.фамилия, с.имя
        ORDER BY тренировок DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
