from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from src.schemas.room import SeatPublic


class Ticket(SQLModel, table=True):
    __tablename__ = 'tickets'

    id: int | None = Field(default=None, primary_key=True)
    session_id: int | None = Field(
        default=None, foreign_key='movie_sessions.id')
    user_id: int | None = Field(default=None, foreign_key='users.id')
    price: int | None = Field(default=None)
    room_id: int | None = Field(default=None, foreign_key='rooms.id')
    movie_id: int | None = Field(default=None, foreign_key='movies.id')
    seat_number: int | None = Field(default=None)
    seat_row: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)


class TicketPublic(BaseModel):
    user_name: str
    room_name: str
    movie_name: str
    price: int
    start_time: datetime
    end_time: datetime
    seat_number: int | None = Field(default=None)
    seat_row: str | None = Field(default=None)


class TicketPublicList(BaseModel):
    tickets: List[TicketPublic] = []


class TicketCreate(BaseModel):
    session_id: int
    seat: Optional[SeatPublic] | None = None
