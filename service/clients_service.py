from repositories.clients_repo import get_all_clients, get_client_by_id, add_client, update_client

def list_clients():
    return get_all_clients()

def get_client(client_id):
    return get_client_by_id(client_id)

def create_client(last_name, first_name, middle_name, phone, email):
    add_client(last_name, first_name, middle_name, phone, email)

def edit_client(client_id, last_name, first_name, middle_name, phone, email):
    update_client(client_id, last_name, first_name, middle_name, phone, email)
