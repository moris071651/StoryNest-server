from uuid import UUID
from . import get_conn


def get_user_by_email(email: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password_hash FROM users WHERE email = %s LIMIT 1", (email,))
            return curr.fetchone()


def get_user_by_name(name: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password_hash FROM users WHERE name = %s", (name,))
            return curr.fetchone()


def insert_user(name: str, email: str, hashed_pw: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (name, email, hashed_pw))

            return curr.fetchone()[0]


def get_user_by_id(user_id: UUID):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password_hash FROM users WHERE id = %s", (str(user_id),))
            return curr.fetchone()


def get_all_users():
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password_hash FROM users")
            return curr.fetchall()
        
def delete_user_by_id(user_id):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("DELETE FROM users WHERE id = %s", (str(user_id),))


def update_user_by_id(story_id, name, email, hashed_pw):
    with get_conn() as conn:
        with conn.cursor() as curr:
            fields = []
            values = []

            if name is not None:
                fields.append("name = %s")
                values.append(name)

            if email is not None:
                fields.append("email = %s")
                values.append(email)

            if hashed_pw is not None:
                fields.append("password_hash = %s")
                values.append(hashed_pw)

            if len(fields) == 0:
                return None

            query = f"""
                UPDATE users
                SET {', '.join(fields)}
                WHERE id = %s
                RETURNING id, name, email, password_hash
            """

            values.append(str(story_id))
            curr.execute(query, values)
            return curr.fetchone()
