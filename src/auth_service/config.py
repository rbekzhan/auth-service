import os

LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s"

DB_USER_NAME = os.environ.get("AUTH_DB_USER_NAME")
DB_USER_PASSWORD = os.environ.get("AUTH_DB_USER_PASSWORD")
DB_NAME = os.environ.get("AUTH_DB_NAME")
DB_HOST = os.environ.get("AUTH_DB_HOST")
DB_PORT = os.environ.get("AUTH_DB_PORT")
DB_DSN = f"postgresql+asyncpg://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SECRET_KEY = 'j3h6xuhcmays446h6f6zfw8sqx9ucfumyzxfppz5rdczkbzux5t9ezzezf7yauzg'
ACCESS_TOKEN_EXPIRATION = 36000
REFRESH_TOKEN_EXPIRATION = 604800