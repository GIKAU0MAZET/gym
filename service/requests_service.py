from repositories.requests_repo import get_all_requests, get_request_by_id, add_request, update_request

def list_requests():
    return get_all_requests()

def get_request(req_id):
    return get_request_by_id(req_id)

def create_request(client_id, type_id, employee_id):
    add_request(client_id, type_id, employee_id)

def edit_request(req_id, client_id, type_id, status):
    update_request(req_id, client_id, type_id, status)
