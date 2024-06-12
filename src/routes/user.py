from fastapi import APIRouter, status

from src.core.dependencies import SessionDep
from src.models.user import create_user
from src.schemas.user import User, UserCreate, UserPublic

user_router = APIRouter()


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_users(user: UserCreate, db: SessionDep):
    new_user = await create_user(session=db, user_create=user)
    return new_user
