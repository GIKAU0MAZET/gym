from datetime import date, timedelta
from repositories.abonements_repo import (
    get_all_abonement_types, get_all_client_abonements,
    get_abonement_by_id, add_client_abonement, update_client_abonement
)

def list_abonement_types():
    return get_all_abonement_types()

def list_client_abonements():
    return get_all_client_abonements()

def get_abonement(abo_id):
    return get_abonement_by_id(abo_id)

def sell_abonement(client_id, type_id, start_date, days, employee_id, request_id=None):
    start = date.fromisoformat(start_date)
    end = start + timedelta(days=int(days))
    number = f"AB-{int(date.today().strftime('%Y%m%d'))}-{client_id}"
    add_client_abonement(client_id, type_id, start, end, number, employee_id, request_id)

def edit_abonement(abo_id, client_id, type_id, start_date, end_date):
    update_client_abonement(abo_id, client_id, type_id, start_date, end_date)
