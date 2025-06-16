from uuid import UUID
from fastapi import APIRouter, Path, Request, Response
from typing import Union, List
from services import story as service

from utils.security import get_auth_user
from exceptions.auth import UnauthenticatedUserException
from schemas.story import StoryCreate, StoryUpdate, StoryInfoPublic, StoryInfoOwner, StoryPublic, StoryOwner


router = APIRouter(prefix='/stories', tags=["Stories"])


@router.get("/")
def list_stories() -> List[StoryInfoPublic]:
    return service.get_pub_stories()


@router.get("/{story_id}")
def get_story_content(request: Request, story_id: UUID = Path(...)) -> Union[StoryPublic, StoryOwner]:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)

    return service.get_story(story_id, user_id)


@router.post("/")
def add_story(request: Request, story: StoryCreate) -> StoryInfoOwner:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    new_story = service.create_story(
        title=story.title,
        subtitle=story.subtitle,
        content=story.content,
        author_id=user_id
    )

    return new_story


@router.patch("/{story_id}")
def update_story(request: Request, story_id: UUID, update: StoryUpdate) -> StoryInfoOwner:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return service.update_story(
        story_id=story_id,
        user_id=user_id,
        title=update.title,
        subtitle=update.subtitle,
        content=update.content
    )


@router.delete("/{story_id}")
def delete_story(request: Request, story_id: UUID):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    service.delete_story(story_id, user_id)


