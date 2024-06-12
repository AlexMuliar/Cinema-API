import jwt
from cachetools import TTLCache
from fastapi import HTTPException, status
from sqlmodel import select

from src.core.config import settings
from src.core.dependencies import SessionDep, TokenDep
from src.schemas.token import TokenData
from src.schemas.user import User, UserPublic

access_token_blocklist = TTLCache(
    maxsize=128, ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
refresh_token_blocklist = TTLCache(
    maxsize=128, ttl=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)


async def _get_current_user(session: SessionDep, token: TokenDep, secret_key: str) -> UserPublic:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenData(username=payload['sub'])
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if access_token_blocklist.get(payload['sub']) == token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User unauthorized",
        )
    user = session.exec(select(User).where(
        User.username == token_data.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.to_user_public()


async def get_current_user(session: SessionDep, token: TokenDep) -> UserPublic:
    return await _get_current_user(session, token, settings.SECRET_KEY)


async def get_current_user_by_refresh_token(session: SessionDep, token: TokenDep) -> UserPublic:
    return await _get_current_user(session, token, settings.REFRESH_SECRET_KEY)


async def get_current_admin_user(session: SessionDep, token: TokenDep) -> UserPublic:
    user = await _get_current_user(session, token, settings.SECRET_KEY)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an admin",
        )
    return user


async def get_current_viewer_user(session: SessionDep, token: TokenDep) -> UserPublic:
    user = await _get_current_user(session, token, settings.SECRET_KEY)
    if not user.is_viewer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a viewer",
        )
    return user
