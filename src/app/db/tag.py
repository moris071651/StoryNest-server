from . import get_conn


def get_all_tags() -> list[tuple[str]]:
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT name FROM tags ORDER BY name")
            return curr.fetchall()


def get_tags_by_story_id(story_id: str) -> list[tuple[str]]:
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                SELECT t.name
                FROM story_tags st
                JOIN tags t ON st.tag_id = t.id
                WHERE st.story_id = %s
                ORDER BY t.name
            """, (story_id,))
            return curr.fetchall()


def add_tags_to_story(story_id: str, tags: list[str]):
    with get_conn() as conn:
        with conn.cursor() as curr:
            for tag in tags:
                curr.execute("INSERT INTO tags (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (tag,))

                curr.execute("""
                    INSERT INTO story_tags (story_id, tag_id)
                    SELECT %s, id FROM tags WHERE name = %s
                    ON CONFLICT DO NOTHING
                """, (story_id, tag))


def remove_tags_from_story(story_id: str, tags: list[str]):
    with get_conn() as conn:
        with conn.cursor() as curr:
            for tag in tags:
                curr.execute("""
                    DELETE FROM story_tags
                    WHERE story_id = %s
                    AND tag_id = (SELECT id FROM tags WHERE name = %s)
                """, (story_id, tag))
