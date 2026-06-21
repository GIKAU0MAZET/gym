from repositories.director_repo import (
    get_gym_info, get_all_employees, get_employee_by_id,
    add_employee, update_employee,
    get_abonement_sales_report, get_active_abonements_report, get_trainer_trainings_report
)

def get_gym():
    return get_gym_info()

def list_employees():
    return get_all_employees()

def get_employee(emp_id):
    return get_employee_by_id(emp_id)

def create_employee(last_name, first_name, middle_name, position, phone, email, hire_date):
    add_employee(last_name, first_name, middle_name, position, phone, email, hire_date)

def edit_employee(emp_id, last_name, first_name, middle_name, position, phone, email, hire_date):
    update_employee(emp_id, last_name, first_name, middle_name, position, phone, email, hire_date)

def report_sales(date_from, date_to):
    return get_abonement_sales_report(date_from, date_to)

def report_active():
    return get_active_abonements_report()

def report_trainers():
    return get_trainer_trainings_report()
