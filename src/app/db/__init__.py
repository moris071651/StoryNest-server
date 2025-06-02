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


with open("src/app/db/init.sql") as f:
    with get_conn() as conn:
        with conn.cursor() as curr:
            curr.execute(f.read())
