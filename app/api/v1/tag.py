from typing import List
from uuid import UUID
from fastapi import APIRouter, Query, Request
from schemas.tag import Tags

from exceptions.auth import UnauthenticatedUserException
from utils.security import get_auth_user
from services import tag as service


router = APIRouter(tags=["Tags"])


@router.get('/tags')
def get_all_tags() -> Tags:
    return service.get_all_tags()


@router.get('/stories/{story_id}/tags')
def get_story_tags(story_id: UUID) -> Tags:
    return service.get_story_tags(story_id)


@router.post('/stories/{story_id}/tags')
def add_story_tag(request: Request, story_id: UUID, tags: List[str] = Query(...)):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id is None:
        raise UnauthenticatedUserException()
    
    service.add_tags_to_story(story_id, user_id, tags)
    return {"detail": "Tags added"}


@router.delete('/stories/{story_id}/tags')
def remove_story_tags(request: Request, story_id: UUID, tags: List[str] = Query(...)):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id is None:
        raise UnauthenticatedUserException()

    service.remove_tags_from_story(story_id, user_id, tags)
    return {"detail": "Tags removed"}
