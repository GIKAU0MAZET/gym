from repositories.trainer_repo import get_trainings_for_trainer
from repositories.trainings_repo import get_training_clients, mark_attendance

def list_my_trainings(employee_id):
    return get_trainings_for_trainer(employee_id)

def get_clients_for_training(tr_id):
    return get_training_clients(tr_id)

def set_attendance(tr_id, client_id, attended):
    mark_attendance(tr_id, client_id, attended)
