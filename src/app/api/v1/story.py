from uuid import UUID
from fastapi import APIRouter, Path,Request, Response
from typing import Union, List
from services.story import create_story, get_story, s_delete_story, s_update_story


from exceptions import handle_errors
from utils.security import get_auth_user
from exceptions.auth import UnauthenticatedUserException
from schemas.story import StoryCreate, StoryUpdate, StoryInfoPublic, StoryInfoOwner, StoryPublic, StoryOwner


router = APIRouter(prefix='/stories', tags=["Stories"])


@router.get("/")
@handle_errors
def list_stories() -> List[StoryInfoPublic]:
    pass


@router.get("/{story_id}")
@handle_errors
def get_story_content(request: Request, story_id: UUID = Path(...)) -> Union[StoryPublic, StoryOwner]:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)

    return get_story(story_id, user_id)


@router.post("/")
@handle_errors
def add_story(request: Request, story: StoryCreate) -> StoryInfoOwner:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    story = create_story(
        title=story.title,
        subtitle=story.subtitle,
        content=story.content,
        author_id=user_id
    )

    return story


@router.patch("/{story_id}")
@handle_errors
def update_story(request: Request, story_id: UUID, update: StoryUpdate) -> StoryInfoOwner:
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()

    return s_update_story(
        story_id=story_id,
        user_id=user_id,
        title=update.title,
        subtitle=update.subtitle,
        content=update.content
    )


@router.delete("/{story_id}")
@handle_errors
def delete_story(request: Request, story_id: UUID):
    token = request.cookies.get('Authorization')
    user_id = get_auth_user(token)
    if user_id == None:
        raise UnauthenticatedUserException()
    
    s_delete_story(story_id, user_id)


