from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field
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
    name: OptionalStr = Field(default=None, min_length=1, max_length=255)
    email: OptionalEmail = Field(default=None, min_length=1, max_length=255)
    password: OptionalStr = Field(default=None, min_length=1, max_length=255)


class LoginStatus(BaseModel):
    is_logged_in: bool
