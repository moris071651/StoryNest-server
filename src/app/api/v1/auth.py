from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Body, Request, Response, status

from exceptions import handle_errors
from services.user import create_user
from utils.security import gen_auth_token
from utils.config import ACCESS_TOKEN_EXPIRE_MINUTES
from exceptions.auth import AuthTokenProvidedException
from schemas.user import UserCredentials, UserInfo, LoginStatus


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED)
@handle_errors
def signup(request: Request, response: Response, user_credentials: UserCredentials = Body(...)) -> UserInfo:
    token = request.cookies.get("Authorization")
    if token:
        raise AuthTokenProvidedException()

    expire_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    user_info = create_user(
        name=user_credentials.name,
        email=user_credentials.email,
        password=user_credentials.password
    )

    token = gen_auth_token(user_info.id, expire_date)
    response.set_cookie(
        key="Authorization",
        value=token,
        httponly=True,
        expires=expire_date,
        samesite="Lax"
    )

    return user_info


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: UserCredentials = Body(...)) -> UserInfo:
    pass

@router.get("/login", status_code=status.HTTP_200_OK)
def is_logged_in() -> LoginStatus:
    pass


@router.post("/logout")
def logout():
    pass
