from uuid import UUID
from schemas.comment import Comment

from db import comment as repo


def create_comment(content: str, author_id: UUID) -> Comment:
    row = repo.insert_comment(content, str(author_id))
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