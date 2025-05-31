from uuid import UUID
from . import get_conn


def get_user_by_email(email: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password FROM users WHERE email = %s LIMIT 1", (email,))
            return curr.fetchone()


def get_user_by_name(name: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password FROM users WHERE name = %s", (name,))
            return curr.fetchone()


def insert_user(name: str, email: str, hashed_pw: str):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (name, email, hashed_pw))

            return curr.fetchone()[0]


def get_user_by_id(user_id: UUID):
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute("SELECT id, name, email, password FROM users WHERE id = %s", (str(user_id),))
            return curr.fetchone()
