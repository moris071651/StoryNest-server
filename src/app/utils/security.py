from datetime import datetime, timezone
from typing import Optional
from jose import jwt
from utils.config import JWT_SECRET, JWT_ALGORITHM
from services.user import verify_user_id
from uuid import UUID


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
