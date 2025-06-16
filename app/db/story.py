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


def get_story_author_by_id(story_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT author_id FROM stories WHERE id = %s", (str(story_id),))
            return curr.fetchone()


def update_story_by_id(story_id: UUID, title: Optional[str], subtitle: Optional[str], content: Optional[str]):
    with get_conn() as conn:
        with conn.cursor() as curr:
            fields = []
            values = []

            if title is not None:
                fields.append("title = %s")
                values.append(title)

            if subtitle is not None:
                fields.append("subtitle = %s")
                values.append(subtitle)

            if content is not None:
                fields.append("content = %s")
                values.append(content)

            if len(fields) == 0:
                return None

            fields.append("updated_at = CURRENT_TIMESTAMP")

            query = f"""
                UPDATE stories
                SET {', '.join(fields)}
                WHERE id = %s
                RETURNING id, title, subtitle,
                         content, author_id, is_published,
                         published_at, created_at, updated_at
            """

            values.append(str(story_id))
            curr.execute(query, values)
            return curr.fetchone()


def delete_story_by_id(story_id):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("DELETE FROM stories WHERE id = %s", (str(story_id),))


def get_pub_by_id(story_id):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT is_published FROM stories WHERE id = %s", (str(story_id),))

            row = curr.fetchone()
            if row != None:
                return row[0]
            else:
                return None
        

def set_pub_by_id(story_id, status):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                UPDATE stories
                SET is_published = %s
                WHERE id = %s
                RETURNING is_published
            """, (status, str(story_id)))

            row = curr.fetchone()
            if row != None:
                return row[0]
            else:
                return None

def get_stories_by_owner_id(author_id):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""SELECT id, title, subtitle, is_published, published_at, created_at, updated_at
                            FROM stories WHERE author_id = %s""", (str(author_id),))

            return curr.fetchall()

def get_stories():
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""SELECT id, title, subtitle, published_at, author_id
                            FROM stories WHERE is_published = TRUE""")

            return curr.fetchall()
