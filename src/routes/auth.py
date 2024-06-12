from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.core.config import settings
from src.core.dependencies import SessionDep, TokenDep
from src.core.logger import get_logger
from src.core.security import create_access_token, create_refresh_token
from src.models.user import authenticate
from src.schemas.token import Token, TokenPair
from src.schemas.user import UserPublic
from src.utils.auth import (access_token_blocklist, get_current_user,
                            get_current_user_by_refresh_token,
                            refresh_token_blocklist)

auth_router = APIRouter()
logger = get_logger(__name__)


async def _get_verified_user(session: Session, form_data: OAuth2PasswordRequestForm) -> UserPublic:
    user = await authenticate(
        session=session,
        login=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def _get_new_token_pair(user: UserPublic) -> TokenPair:
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=access_token_expires * 24
    )
    return TokenPair(
        access_token=Token(access_token=access_token, token_type="bearer"),
        refresh_token=Token(access_token=refresh_token, token_type="bearer"),
    )


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = await _get_verified_user(session, form_data)
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.post("/")
async def login_for_access_token_pair(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> TokenPair:
    user = await _get_verified_user(session, form_data)
    return _get_new_token_pair(user)


@auth_router.post('/refresh',
                  dependencies=[Depends(get_current_user_by_refresh_token)],
                  response_model=TokenPair
                  )
async def create_new_token_pair(
    current_user: Annotated[UserPublic, Depends(get_current_user_by_refresh_token)],
    token: TokenDep,
) -> TokenPair:
    refresh_token_blocklist[current_user.username] = token
    return _get_new_token_pair(current_user)


@auth_router.post(
    '/logout',
    dependencies=[Depends(get_current_user)],
)
async def logout(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
    token: TokenDep,
) -> dict:
    access_token_blocklist[current_user.username] = token
    return {"message": "Successfully logged out"}


@auth_router.get("/useraccount", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
):
    return current_user
