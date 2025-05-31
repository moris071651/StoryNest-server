from fastapi import APIRouter, Body, Path
from typing import Union, List

from schemas.story import StoryCreate, StoryUpdate, StoryInfoPublic, StoryInfoOwner, StoryPublic, StoryOwner


router = APIRouter(prefix='/stories', tags=["Stories"])


@router.get("/")
def list_stories() -> List[StoryInfoPublic]:
    pass


@router.get("/{story_id}")
def get_story(story_id: int = Path(...)) -> Union[StoryPublic, StoryOwner]:
    pass


@router.post("/")
def create_story(story: StoryCreate) -> StoryInfoOwner:
    pass


@router.patch("/{story_id}")
def update_story(story_id: int, update: StoryUpdate) -> StoryInfoOwner:
    pass


@router.delete("/{story_id}")
def delete_story(story_id: int):
    pass
