from db.user import get_user_by_email, insert_user
from exceptions.auth import UserAlreadyExistsException
from schemas.user import UserInfo
from utils.password import hash_password


def create_user(name: str, email: str, password: str) -> UserInfo:    
    existing_user = get_user_by_email(email)
    if existing_user:
        raise UserAlreadyExistsException()

    hashed_pw = hash_password(password)
    user_id = insert_user(name, email, hashed_pw)

    return UserInfo(id=user_id, name=name, email=email)
