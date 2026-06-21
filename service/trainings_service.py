from repositories.trainings_repo import (
    get_all_trainings, get_training_by_id, add_training, update_training,
    get_training_clients, enroll_client, mark_attendance
)

def list_trainings():
    return get_all_trainings()

def get_training(tr_id):
    return get_training_by_id(tr_id)

def create_training(employee_id, hall_id, datetime_val, name, max_participants):
    add_training(employee_id, hall_id, datetime_val, name, max_participants)

def edit_training(tr_id, employee_id, datetime_val, name, max_participants):
    update_training(tr_id, employee_id, datetime_val, name, max_participants)

def get_clients_of_training(tr_id):
    return get_training_clients(tr_id)

def add_client_to_training(tr_id, client_id):
    enroll_client(tr_id, client_id)

def set_attendance(tr_id, client_id, attended):
    mark_attendance(tr_id, client_id, attended)
