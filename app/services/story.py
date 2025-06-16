from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID
from schemas.story import StoryInfoOwner, StoryInfoPublic, StoryOwner, StoryPublic
from db.story import get_stories, get_stories_by_owner_id, get_story_author_by_id, insert_story, get_story_by_id, delete_story_by_id, update_story_by_id, get_pub_by_id, set_pub_by_id
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
        if is_published:
            return StoryPublic(
                id=id,
                title=title,
                subtitle=subtitle,
                author_id=author_id,
                published_at=published_at,
                content=content
            )
        else:
            raise UnauthorizedOperationException()
        

def get_pub_stories() -> List[StoryInfoPublic]:
    rows = get_stories()
    if rows == None:
        raise Exception()
    
    return [
        StoryInfoPublic(
            id=id,
            title=title,
            subtitle=subtitle,
            published_at=published_at,
            author_id=author_id
        )
        for id, title, subtitle, published_at, author_id in rows
    ]



def update_story(
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
    _, _,is_published,
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


def delete_story(story_id: UUID, user_id: UUID):
    row = get_story_author_by_id(str(story_id))
    if row == None:
        raise NoSuchStoryException()
    
    if row[0] != user_id:
        raise UnauthorizedOperationException()
    
    delete_story_by_id(str(story_id))


def get_pub_status(story_id: UUID, user_id: UUID) -> bool:
    row = get_story_author_by_id(str(story_id))
    if row == None:
        raise NoSuchStoryException()
    
    (author_id,) = row
    if author_id != user_id:
        raise UnauthorizedOperationException()
    
    status = get_pub_by_id(str(story_id))

    return status


def set_pub_status(user_id: UUID, story_id: UUID, status: bool):
    row = get_story_author_by_id(str(story_id))
    if row == None:
        raise NoSuchStoryException()
    
    (author_id,) = row
    if author_id != user_id:
        raise UnauthorizedOperationException()

    status = set_pub_by_id(str(story_id), status)

    return status

def get_user_story(user_id: UUID, is_owner: bool) -> Union[List[StoryInfoPublic], List[StoryInfoOwner]]:
    rows = get_stories_by_owner_id(str(user_id))
    if rows == None:
        raise Exception()
    
    if is_owner:
        return [
            StoryInfoOwner(
                id=id,
                title=title,
                subtitle=subtitle,
                is_published=is_published,
                published_at=published_at,
                created_at=created_at,
                updated_at=updated_at
            )
            for id, title, subtitle, is_published, published_at, created_at, updated_at in rows
        ]
    
    else:
        return [
            StoryInfoPublic(
                id=id,
                title=title,
                subtitle=subtitle,
                published_at=published_at,
            )
            for id, title, subtitle, is_published, published_at, _, _ in rows
            if is_published is True
        ]
