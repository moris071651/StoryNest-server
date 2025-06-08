from typing import List
from fastapi import APIRouter, Query, Request

from exceptions.auth import UnauthenticatedUserException
from utils.security import get_auth_user


router = APIRouter(tags=["Tags"])


@router.get('/tags')
def get_all_tags():
    pass


@router.get('/stories/{story_id}/tags')
def get_story_tags():
    pass


@router.post('/stories/{story_id}/tags')
def add_story_tag(request: Request):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()


@router.delete('/stories/{story_id}/tags')
def remove_story_tags(request: Request, tags: List[str] = Query()):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
