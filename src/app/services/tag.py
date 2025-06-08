from uuid import UUID
from db.story import get_story_author_by_id
from exceptions.auth import UnauthorizedOperationException
from exceptions.story import NoSuchStoryException
from schemas.tag import Tags
from db import tag as repo

def get_all_tags() -> Tags:
    rows = repo.get_all_tags()
    return Tags(tags=[row[0] for row in rows])


def get_story_tags(story_id: UUID) -> Tags:
    rows = repo.get_tags_by_story_id(str(story_id))
    return Tags(tags=[row[0] for row in rows])


def add_tags_to_story(story_id: UUID, user_id: UUID, tags: list[str]):
    row = get_story_author_by_id(str(story_id))
    if row == None:
        raise NoSuchStoryException()
    
    if row[0] != user_id:
        raise UnauthorizedOperationException()

    repo.add_tags_to_story(str(story_id), tags)


def remove_tags_from_story(story_id: UUID, user_id: UUID, tags: list[str]):
    row = get_story_author_by_id(str(story_id))
    if row == None:
        raise NoSuchStoryException()
    
    if row[0] != user_id:
        raise UnauthorizedOperationException()

    repo.remove_tags_from_story(str(story_id), tags)
