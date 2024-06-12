from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    return _create_token(
        data=data,
        secret_key=settings.SECRET_KEY,
        expires_delta=expires_delta,
    )


def create_refresh_token(data: dict, expires_delta: timedelta) -> str:
    return _create_token(
        data=data,
        secret_key=settings.REFRESH_SECRET_KEY,
        expires_delta=expires_delta,
    )


def _create_token(data: dict, secret_key: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        secret_key,
        algorithm=settings.ALGORITHM)
    return encoded_jwt
