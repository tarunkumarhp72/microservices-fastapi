from jose import jwt, JWTError

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None