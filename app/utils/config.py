import os

JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/db_sn")
