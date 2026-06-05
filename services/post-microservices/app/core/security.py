from jose import jwt, JWTError
import os
from dotenv import load_dotenv
load_dotenv()



secret_key_from_env = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            secret_key_from_env,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None