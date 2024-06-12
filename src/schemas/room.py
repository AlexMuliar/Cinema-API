from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class RoomTypeEnum(Enum):
    open_space = 1
    fixed_seats = 2


class RoomType(SQLModel, table=True):
    __tablename__ = 'room_types'

    id: int | None = Field(default=None, primary_key=True)
    name: RoomTypeEnum


class Room(SQLModel, table=True):
    __tablename__ = 'rooms'

    id: int = Field(default=None, primary_key=True)
    name: str
    capacity: int
    type: int = Field(default=1, foreign_key="room_types.id")
    seats: Optional[List['Seat']] = Relationship(back_populates="room")

    @property
    def is_open_space(self):
        return self.type == RoomType.open_space

    @property
    def is_fixed_seats(self):
        return self.type == RoomType.fixed_seats


class Seat(SQLModel, table=True):
    __tablename__ = 'seats'

    id: int = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="rooms.id")
    row: str
    number: int
    room: Optional[Room] = Relationship(back_populates="seats")


class SeatPublic(BaseModel):
    row: str
    number: int
