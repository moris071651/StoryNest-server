from datetime import datetime, timezone
from typing import Optional
from fastapi import Request
from jose import jwt
from uuid import UUID

try:
    from exceptions.auth import UnauthenticatedUserException
    from utils.config import JWT_SECRET, JWT_ALGORITHM
    from services.user import verify_user_id
except ModuleNotFoundError:
    from app.services.user import verify_user_id
    from app.exceptions.auth import UnauthenticatedUserException
    from app.utils.config import JWT_SECRET, JWT_ALGORITHM

def valid_expire_date(expire_date):
    if isinstance(expire_date, str):
        expire_date = datetime.fromisoformat(expire_date)

    elif not isinstance(expire_date, datetime):
        return False
    
    if expire_date.tzinfo is None:
        expire_date = expire_date.replace(tzinfo=timezone.utc)

    return expire_date >= datetime.now(timezone.utc)


def gen_auth_token(user_id: UUID, expire_date: datetime) -> str:
    data = {
        "user_id": str(user_id),
        "expire": expire_date.isoformat(),
    }

    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_auth_token(token: Optional[str]) -> bool:
    if token == None:
        return False
    
    try:
        payload: dict = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)

        user_id = payload.get("user_id")
        if not verify_user_id(user_id):
            return False

        expire_date = payload.get('expire')
        if not valid_expire_date(expire_date):
            return False
        
        return True

    except Exception:
        pass

    return False


def get_auth_data(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_auth_user(token: str) -> Optional[UUID]:
    if token == None:
        return None
    
    try:
        payload: dict = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)

        user_id = payload.get("user_id")
        if not verify_user_id(user_id):
            return None

        expire_date = payload.get('expire')
        if not valid_expire_date(expire_date):
            return None
        
        return UUID(user_id)

    except Exception:
        pass

    return None


def auth_user(request: Request):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)

    if user_id == None:
        raise UnauthenticatedUserException()
    
    return user_id
