from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from uuid import UUID


OptionalStr = Annotated[Optional[str], None]


class StoryInfoBase(BaseModel):
    id: UUID
    title: str
    subtitle: OptionalStr


class StoryInfoPublic(StoryInfoBase):
    author_id: UUID
    published_at: datetime


class StoryInfoOwner(StoryInfoBase):
    is_published: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class StoryPublic(StoryInfoPublic):
    content: str


class StoryOwner(StoryInfoOwner):
    content: str


class StoryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    subtitle: OptionalStr = Field(default=None, min_length=1, max_length=255)
    content: OptionalStr = Field(default=None, min_length=1)

class StoryUpdate(BaseModel):
    title: OptionalStr = Field(default=None, min_length=1, max_length=255)
    subtitle: OptionalStr = Field(default=None, min_length=1, max_length=255)
    content: OptionalStr = Field(default=None, min_length=1)
