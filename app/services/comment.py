from typing import Optional
from uuid import UUID
from schemas.comment import Comment

from db import comment as repo

def get_comment(story_id: UUID, comment_id: UUID):
    row = repo.get_comment_story_by_id(str(comment_id))
    if row == None:
        raise Exception()
    
    if row[0] != story_id:
        raise Exception()

    row = repo.get_comment_by_id(str(comment_id))
    if row is None:
        raise Exception()

    id, story_id, author_id, content, created_at, updated_at = row

    return Comment(
        id=id,
        story_id=story_id,
        author_id=author_id,
        content=content,
        created_at=created_at,
        updated_at=updated_at
    )


def get_comments(story_id: UUID) -> list[Comment]:
    rows = repo.get_comments_by_story_id(str(story_id))
    return [
        Comment(
            id=row[0],
            story_id=row[1],
            author_id=row[2],
            content=row[3],
            created_at=row[4],
            updated_at=row[5]
        )
        for row in rows
    ]


def create_comment(content: str, author_id: UUID, story_id: UUID) -> Comment:
    row = repo.insert_comment(content, str(author_id), str(story_id))
    if row == None:
        raise Exception()
    
    (id, story_id, author_id, content, created_at, updated_at) = row

    return Comment(
        id=id,
        story_id=story_id,
        author_id=author_id,
        content=content,
        created_at=created_at,
        updated_at=updated_at
    )


def update_comment(user_id: UUID, story_id: UUID, comment_id: UUID, content: str):
    row = repo.get_comment_author_by_id(str(comment_id))
    if row == None:
        raise Exception()
    
    if row[0] != user_id:
        raise Exception()
    
    row = repo.get_comment_story_by_id(str(comment_id))
    if row == None:
        raise Exception()
    
    if row[0] != story_id:
        raise Exception()
        
    row = repo.update_comment_by_id(content=content, comment_id=str(comment_id))
    if row == None:
        raise Exception()
    
    (id, story_id, author_id, content, created_at, updated_at) = row

    return Comment(
        id=id,
        story_id=story_id,
        author_id=author_id,
        content=content,
        created_at=created_at,
        updated_at=updated_at
    )


def delete_comment(user_id: UUID, story_id: UUID, comment_id: UUID):
    row = repo.get_comment_author_by_id(str(comment_id))
    if row is None:
        raise Exception()

    if row[0] != user_id:
        raise Exception()

    row = repo.get_comment_story_by_id(str(comment_id))
    if row is None:
        raise Exception()

    if row[0] != story_id:
        raise Exception()

    row = repo.delete_comment_by_id(str(comment_id))
    if row is None:
        raise Exception()
