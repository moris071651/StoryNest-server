from contextlib import contextmanager
from utils.config import POSTGRES_URL
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    POSTGRES_URL,
    max_size=10,
    max_idle=5,
    timeout=10
)

@contextmanager
def get_conn():
    with pool.connection() as conn:
        yield conn

with get_conn() as conn:
    with conn.cursor() as curr:
        curr.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

with get_conn() as conn:
    with conn.cursor() as curr:
        curr.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
