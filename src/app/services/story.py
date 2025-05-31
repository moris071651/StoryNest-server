from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from schemas.story import StoryInfoOwner, StoryOwner, StoryPublic
from db.story import insert_story, get_story_by_id

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
