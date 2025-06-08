from . import get_conn


def insert_comment(content: str, author_id: str, story_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO comments (story_id, author_id, content)
                VALUES (%s, %s, %s)
                RETURNING id, story_id, author_id, content, created_at, updated_at
            """, (content, author_id, story_id))

            return curr.fetchone()
