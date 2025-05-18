import os

from dotenv import load_dotenv
from fastapi import HTTPException, Request
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")  # Load SECRET_KEY from environment variables
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables")
ALGORITHM = "HS256"


def authenticate_user(request: Request):
    """
    Authenticate the user by validating the JWT token stored in cookies.
    Extract the user_id from the token and return it.
    """
    token = request.cookies.get("access-token")
    if not token:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")  # Extract the user_id from the payload
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        return user_id  # Return the user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
