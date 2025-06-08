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


def get_comment_author_by_id(comment_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT author_id FROM comments WHERE id = %s", (comment_id,))
            return curr.fetchone()


def get_comment_story_by_id(comment_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT story_id FROM comments WHERE id = %s", (comment_id,))
            return curr.fetchone()


def update_comment_by_id(content: str, comment_id: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                UPDATE comments
                SET content = %s
                WHERE id = %s
                RETURNING id, story_id, author_id, content, created_at, updated_at
            """, (content, comment_id))

            return curr.fetchone()
