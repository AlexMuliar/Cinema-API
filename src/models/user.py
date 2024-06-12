from sqlmodel import Session, select
from validator_collection import is_email

from src.core.security import get_password_hash, verify_password
from src.schemas.user import User, UserCreate, UserPublic


async def create_user(*, session: Session, user_create: UserCreate) -> UserPublic:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(
            user_create.plain_password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


async def get_user_by_email(*, session: Session, email: str) -> UserPublic | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


async def get_user_by_username(*, session: Session, username: str) -> UserPublic | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user


async def authenticate(*, session: Session, login: str, password: str) -> UserPublic | None:
    if is_email(login):
        db_user = await get_user_by_email(session=session, email=login)
    else:
        db_user = await get_user_by_username(session=session, username=login)

    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
