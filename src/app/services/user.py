from typing import Optional
from uuid import UUID
from exceptions.user import EmailAlreadyTakenException
from db.user import get_user_by_email, get_user_by_id, insert_user
from exceptions.auth import InvalidCredentialsException, UserAlreadyExistsException
from schemas.user import UserInfo
from utils.password import hash_password, verify_password
import db.user as model
from psycopg.errors import UniqueViolation


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


def get_all_users():
    row = model.get_all_users()
    if row == None:
        raise Exception()
    
    [UserInfo(
        id=id,
        email=email,
        name=name
    ) for (id, name, email, _) in row]

    return [
        UserInfo(
            id=id,
            email=email,
            name=name
        )
        for (id, name, email, _) in row
    ]


def get_user(user_id: UUID) -> UserInfo:
    row = model.get_user_by_id(user_id)
    if row == None:
        raise Exception()
    
    (id, name, email, _) = row

    return UserInfo(
        id=id,
        email=email,
        name=name
    )


def delete_user(user_id: UUID):
    model.delete_user_by_id(str(user_id))


def update_user(
    name: Optional[str],
    email: Optional[str],
    password: Optional[str],
    user_id: UUID
) -> UserInfo:
    hashed_pw = None
    if password != None:
        hashed_pw = hash_password(password)

    try:
        row = model.update_user_by_id(str(user_id), name, email, hashed_pw)
    except UniqueViolation:
        raise EmailAlreadyTakenException()
    if row == None:
        raise Exception()
    
    (id, name, email, _) = row

    return UserInfo(id=id, name=name, email=email)
