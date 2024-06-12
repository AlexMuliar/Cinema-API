from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class MovieSession(SQLModel, table=True):
    __tablename__ = 'movie_sessions'

    id: int | None = Field(default=None, primary_key=True)
    movie_id: int | None = Field(default=None, foreign_key='movies.id')
    room_id: int | None = Field(default=None, foreign_key='rooms.id')
    start_time: datetime | None = Field(default=None)
    end_time: datetime | None = Field(default=None)


class MovieSessionPublic(BaseModel):
    id: int
    movie_name: str
    room_name: str
    start_time: datetime
    end_time: datetime
    available_seats_amount: int
    available_seats: Optional[List[dict]] = []
    room_type: str


class MovieSessionsPublicList(BaseModel):
    sessions: List[MovieSessionPublic] = []
