from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr
from uuid import UUID

OptionalEmail = Annotated[Optional[EmailStr], None]
OptionalStr = Annotated[Optional[str], None]

class UserInfo(BaseModel):
    id: UUID
    email: EmailStr
    name: str


class UserCredentials(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: OptionalStr
    email: OptionalEmail
    password: OptionalStr


class LoginStatus(BaseModel):
    is_logged_in: bool
