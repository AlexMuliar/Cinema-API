from sqlmodel import Session, func, select

from src.schemas.movie import Movie
from src.schemas.room import Room, RoomTypeEnum, Seat
from src.schemas.session import (MovieSession, MovieSessionPublic,
                                 MovieSessionsPublicList)
from src.schemas.ticket import Ticket


async def get_all_session(session: Session) -> list[MovieSessionPublic]:
    statement = select(MovieSession).order_by(MovieSession.start_time)
    return session.exec(statement).all()


def _get_public_sessions_query(session):
    return select(
        Room,
        MovieSession.id,
        (Room.capacity - func.count(Ticket.id)).label("available_seats_amount"),
        Movie.name,
        MovieSession.start_time,
        MovieSession.end_time
    )\
        .join(MovieSession, Movie.id == MovieSession.movie_id)\
        .join(Room, MovieSession.room_id == Room.id)\
        .outerjoin(Ticket, Ticket.session_id == MovieSession.id)\
        .group_by(
        MovieSession.id,
        Room.capacity,
        Room,
        Movie.name,
        MovieSession.start_time,
        MovieSession.end_time
    )


def _get_available_seats_for_session(db: Session, session_id: int, room_id: int) -> list[dict]:
    available_seats = [
        {
            "row": seat.row,
            "number": seat.number,
        } for seat in db.exec(select(Seat).where(Seat.room_id == room_id)).all()
    ]
    ordered_tickets = db.exec(select(Ticket).where(
        Ticket.session_id == session_id)).all()
    for ticket in ordered_tickets:
        if index := available_seats.index({
            "row": ticket.seat_row,
            "number": ticket.seat_number,
        }):
            available_seats.pop(index)
    return available_seats


async def get_public_sessions_list(session: Session) -> MovieSessionsPublicList:
    statement = _get_public_sessions_query(session)
    query_result = session.exec(statement).all()
    movie_session_list = MovieSessionsPublicList()
    for room, session_id, available_seats_amount, \
            movie_name, start_time, end_time in query_result:

        if available_seats_amount > 0 and room.type == RoomTypeEnum.fixed_seats.value:
            available_seats = _get_available_seats_for_session(
                session, session_id, room.id)
        else:
            available_seats = []

        movie_session_list.sessions.append(MovieSessionPublic(
            id=session_id,
            available_seats_amount=available_seats_amount,
            movie_name=movie_name,
            room_name=room.name,
            room_type=RoomTypeEnum(room.type).name,
            start_time=start_time,
            end_time=end_time,
            available_seats=available_seats
        ))
    return movie_session_list
