import jwt

from auth_service.config import SECRET_KEY, redis_client
from auth_service.exception import ExpiredSignatureError


def extract_user_id_from_token(token: str) -> str:
    try:
        token: str = token.split(' ')[1]
        blacklist_tokens = redis_client.smembers("blacklist_access_tokens")
        if token.encode('utf-8') in blacklist_tokens:
            raise ValueError("Token is blacklisted")
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], verify=False)
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError(message="Время действия токена истекло", code=4)
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except ValueError as e:
        raise e
    except Exception as e:
        raise e  # перехватить другие исключения здесь, если это необходимо

