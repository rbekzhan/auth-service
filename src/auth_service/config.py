import os

import redis

LOGGING_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s"

HTTP_PROTOCOL = "http"
DB_SERVICE_IP = os.environ.get("DB_SERVICE_IP")
DB_SERVICE_PORT = os.environ.get("DB_SERVICE_PORT")
DB_SERVICE_URL = f"{HTTP_PROTOCOL}://{DB_SERVICE_IP}:{DB_SERVICE_PORT}"

SECRET_KEY = 'j3h6xuhcmays446h6f6zfw8sqx9ucfumyzxfppz5rdczkbzux5t9ezzezf7yauzg'
ACCESS_TOKEN_EXPIRATION = 36000
REFRESH_TOKEN_EXPIRATION = 604800
redis_client = redis.Redis(host='redis', port=6379, db=0)

RABBITMQ_HOST = os.environ.get("RABBITMQ_SERVICE_HOST")
RABBITMQ_PORT = os.environ.get("RABBITMQ_SERVICE_PORT")
RABBITMQ_USER_NAME = os.environ.get("RABBITMQ_SERVICE_USER_NAME")
RABBITMQ_USER_PASSWORD = os.environ.get("RABBITMQ_SERVICE_USER_PASSWORD")
RABBITMQ_AMQP = f"amqp://{RABBITMQ_USER_NAME}:{RABBITMQ_USER_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
