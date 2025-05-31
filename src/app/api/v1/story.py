from uuid import UUID
from fastapi import APIRouter, Body, Path,Request
from typing import Union, List
from services.story import create_story, get_story


from exceptions import handle_errors
from utils.security import get_auth_user
from exceptions.auth import UnauthenticatedUserException
from schemas.story import StoryCreate, StoryUpdate, StoryInfoPublic, StoryInfoOwner, StoryPublic, StoryOwner


router = APIRouter(prefix='/stories', tags=["Stories"])


@router.get("/")
def list_stories() -> List[StoryInfoPublic]:
    pass


@router.get("/{story_id}")
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
def update_story(story_id: int, update: StoryUpdate) -> StoryInfoOwner:
    pass


@router.delete("/{story_id}")
def delete_story(story_id: int):
    pass
