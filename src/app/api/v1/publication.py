from fastapi import APIRouter, Body, Path

from schemas.story import StoryCreate, StoryUpdate, StoryInfoOwner


router = APIRouter(prefix='/stories', tags=["Publication"])


@router.get("/{story_id}/publish")
def get_publication_status(story_id: int):
    pass


@router.put("/{story_id}/publish")
def toggle_publication_status(story_id: int):
    pass


@router.post("/{story_id}/publish")
def publish_story(story_id: int):
    pass


@router.delete("/{story_id}/publish")
def unpublish_story(story_id: int):
    pass
