from db.user import get_user_by_email, get_user_by_id, insert_user
from exceptions.auth import InvalidCredentialsException, UserAlreadyExistsException
from schemas.user import UserInfo
from utils.password import hash_password, verify_password


def create_user(name: str, email: str, password: str) -> UserInfo:    
    existing_user = get_user_by_email(email)
    if existing_user:
        raise UserAlreadyExistsException()

    hashed_pw = hash_password(password)
    user_id = insert_user(name, email, hashed_pw)

    return UserInfo(id=user_id, name=name, email=email)


def authenticate_user(email: str, password: str) -> UserInfo:
    user_row = get_user_by_email(email)
    if user_row == None:
        raise InvalidCredentialsException()

    user_id, name, email, hashed_password = user_row

    if not verify_password(password, hashed_password):
        raise InvalidCredentialsException()

    return UserInfo(id=user_id, name=name, email=email)


def verify_user_id(user_id: str):
    if user_id != None:
        return get_user_by_id(user_id) is not None
    
    return False
