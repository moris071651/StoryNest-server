from typing import Optional
from uuid import UUID

from . import get_conn


def insert_story(title: str, subtitle: Optional[str], content: str, author_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO stories (title, subtitle, content, author_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, is_published, published_at, created_at, updated_at
            """, (title, subtitle, content, str(author_id)))

            return curr.fetchone()
        

def get_story_by_id(story_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""SELECT id, title, subtitle,
                         content, author_id, is_published,
                         published_at, created_at, updated_at
                         FROM stories WHERE id = %s""", (str(story_id),))

            return curr.fetchone()




