import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cms:cms@db:5432/cms"
)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 30
