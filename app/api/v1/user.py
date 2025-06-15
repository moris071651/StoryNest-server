from typing import List
from uuid import UUID
from fastapi import APIRouter, Request, Response, Body
from schemas.user import UserInfo, UserUpdate
from schemas.story import StoryInfoOwner, StoryInfoPublic 
from exceptions.auth import UnauthenticatedUserException
from utils.security import get_auth_user
import services.story as storyService
import services.user as service


router = APIRouter(prefix='/users', tags=["Users"])


@router.get("/")
def get_all_users() -> List[UserInfo]:
    return service.get_all_users()

@router.get("/me")
def get_me(request: Request) -> UserInfo:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return service.get_user(user_id)


@router.get("/me/stories")
def get_me(request: Request) -> List[StoryInfoOwner]:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return storyService.get_user_story(user_id, True)


@router.get("/{user_id}")
def get_user(user_id: UUID) -> UserInfo:
    return service.get_user(user_id)


@router.get("/{user_id}/stories")
def get_user(user_id: UUID) -> List[StoryInfoPublic]:
    return storyService.get_user_story(user_id, False)


@router.patch('/me')
def update_me(request: Request, update: UserUpdate = Body()) -> UserInfo:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    return service.update_user(
        name=update.name,
        email=update.email,
        password=update.password,
        user_id=user_id
    )


@router.delete('/me')
def delete_me(request: Request, response: Response):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    response.delete_cookie(key="Authorization", httponly=True, samesite="Lax")

    service.delete_user(user_id)
