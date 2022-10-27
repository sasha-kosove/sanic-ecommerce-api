import os

app_config = {
    "JWT_SECRET": os.environ.get("JWT_SECRET"),
    "JWT_ALGORITHM": "HS256",
    "EXPIRATION_DELTA": 60 * 60 * 3,
    "TRANSACTION_PRIVATE_KEY": os.environ.get("TRANSACTION_PRIVATE_KEY"),
}

POSTGRES_DB = os.environ.get("POSTGRES_DB", default="postgres")
POSTGRES_USER = os.environ.get("POSTGRES_DB", default="postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_DB", default="postgres")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", default="localhost")
