from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from schemas.story import StoryInfoOwner, StoryOwner, StoryPublic
from db.story import get_story_author_by_id, insert_story, get_story_by_id, delete_story_by_id, update_story_by_id
from exceptions.story import NoSuchStoryException
from exceptions.auth import UnauthorizedOperationException


def create_story(
    title: str,
    subtitle: Optional[str],
    content: Optional[str],
    author_id: UUID
) -> StoryInfoOwner: 
    content = content or ""

    story_id, is_published, published_at, created_at, updated_at = insert_story(
        title, subtitle, content, str(author_id)
    )

    return StoryInfoOwner(
        id=story_id,
        title=title,
        subtitle=subtitle,
        is_published=is_published,
        published_at=published_at,
        created_at=created_at,
        updated_at=updated_at
    )

def get_story(story_id: UUID, user_id: UUID) -> Union[StoryPublic, StoryOwner]:
    (id, title, subtitle,
        content, author_id,is_published,
        published_at, created_at, updated_at) = get_story_by_id(str(story_id))
    
    if author_id == user_id:
        return StoryOwner(
            id=id,
            title=title,
            subtitle=subtitle,
            is_published=is_published,
            published_at=published_at,
            created_at=created_at,
            updated_at=updated_at,
            content=content
        )
    else:
        return StoryPublic(
            id=id,
            title=title,
            subtitle=subtitle,
            author_id=author_id,
            published_at=published_at,
            content=content
        )


def s_update_story(
    story_id: UUID,
    user_id: UUID,
    title: Optional[str],
    subtitle: Optional[str],
    content: Optional[str]
) -> StoryInfoOwner:
    (author_id,) = get_story_author_by_id(str(story_id))
    if author_id == None:
        raise NoSuchStoryException()
    
    if author_id != user_id:
        raise UnauthorizedOperationException()
    
    row = update_story_by_id(str(story_id), title, subtitle, content)
    if row == None:
        return None
    
    (id, title, subtitle,
    content, author_id,is_published,
    published_at, created_at, updated_at) = row

    return StoryInfoOwner(
        id=id,
        title=title,
        subtitle=subtitle,
        is_published=is_published,
        published_at=published_at,
        created_at=created_at,
        updated_at=updated_at
    )


def s_delete_story(story_id: UUID, user_id: UUID):
    (author_id,) = get_story_author_by_id(str(story_id))
    if author_id == None:
        raise NoSuchStoryException()
    
    if author_id != user_id:
        raise UnauthorizedOperationException()
    
    delete_story_by_id(str(story_id))