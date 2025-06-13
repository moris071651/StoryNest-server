from fastapi import APIRouter, Request
from uuid import UUID
from schemas.story import PublicationStatus
from exceptions.auth import UnauthenticatedUserException
from utils.security import get_auth_user

from services.story import set_pub_status, get_pub_status


router = APIRouter(prefix='/stories', tags=["Publication"])


@router.get("/{story_id}/publish")
def get_publication_status(request: Request, story_id: UUID) -> PublicationStatus:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return PublicationStatus(
        is_published=get_pub_status(story_id, user_id)
    )


@router.put("/{story_id}/publish")
def toggle_publication_status(request: Request, story_id: UUID) -> PublicationStatus:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return PublicationStatus(
        is_published=set_pub_status(user_id, story_id, not get_pub_status(story_id, user_id))
    )


@router.post("/{story_id}/publish")
def publish_story(request: Request, story_id: UUID) -> PublicationStatus:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return PublicationStatus(
        is_published=set_pub_status(user_id, story_id, True)
    )


@router.delete("/{story_id}/publish")
def unpublish_story(request: Request, story_id: UUID) -> PublicationStatus:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return PublicationStatus(
        is_published=set_pub_status(user_id, story_id, False)
    )

