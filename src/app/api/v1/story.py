from fastapi import APIRouter, Body, Path


router = APIRouter(prefix='/users')


@router.get("/")
def list_stories():
    pass


@router.get("/{story_id}")
def get_story(story_id: int = Path(...)):
    pass


@router.post("/")
def create_story(story):
    pass


@router.patch("/{story_id}")
def update_story(story_id: int, update):
    pass


@router.delete("/{story_id}")
def delete_story(story_id: int):
    pass


@router.get("/{story_id}/publish")
def get_publish_status(story_id: int):
    pass


@router.put("/{story_id}/publish")
def publish_story(story_id: int, settings = Body(...)):
    pass


@router.post("/{story_id}/publish")
def trigger_publish_action(story_id: int):
    pass


@router.delete("/{story_id}/publish")
def unpublish_story(story_id: int):
    pass
