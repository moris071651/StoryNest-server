from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID
from pydantic import BaseModel


class Comment(BaseModel):
    id: UUID
    story_id: UUID
    author_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: Annotated[Optional[str], None]

