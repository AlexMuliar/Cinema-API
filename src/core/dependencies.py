from typing import Annotated, Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from src.core.db import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="oauth/token")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
