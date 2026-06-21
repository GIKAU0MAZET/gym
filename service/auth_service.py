import bcrypt
from repositories.auth_repo import get_user_by_login

def authenticate(login, password):
    user = get_user_by_login(login)
    if not user:
        return None
    stored_hash = user[2].strip()
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return user
    return None
