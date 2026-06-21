from database import get_connection

def get_trainings_for_trainer(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            т.id_тренировки,
            т.название_тренировки,
            т.дата_время,
            т.максимальное_участников,
            COUNT(кт.id_клиента) AS записано
        FROM тренировки т
        LEFT JOIN клиенты_тренировки кт ON кт.id_тренировки = т.id_тренировки
        WHERE т.id_сотрудника = %s
        GROUP BY т.id_тренировки
        ORDER BY т.дата_время DESC
    """, (employee_id,))
    rows = cur.fetchall()
    conn.close()
    return rows
