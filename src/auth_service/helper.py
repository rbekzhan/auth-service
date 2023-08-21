import jwt

from auth_service.config import SECRET_KEY


def extract_user_id_from_token(token):
    try:
        token: str = token.split(' ')[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'], verify=False)
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
