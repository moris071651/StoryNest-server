from typing import List
from pydantic import BaseModel


class Tags(BaseModel):
    tags: List[str]
