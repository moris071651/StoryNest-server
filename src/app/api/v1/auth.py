from fastapi import APIRouter, Body, status

from schemas.user import UserCredentials, UserInfo, LoginStatus


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def signup(user_credentials: UserCredentials = Body(...)) -> UserInfo:
    pass


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: UserCredentials = Body(...)) -> UserInfo:
    pass

@router.get("/login", status_code=status.HTTP_200_OK)
def is_logged_in() -> LoginStatus:
    pass


@router.post("/logout")
def logout():
    pass
