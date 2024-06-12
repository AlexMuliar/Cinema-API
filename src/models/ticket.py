from typing import List

from sqlmodel import Session, func, select

from src.core.logger import get_logger
from src.models.user import get_user_by_username
from src.schemas.movie import Movie
from src.schemas.room import Room, RoomTypeEnum, Seat
from src.schemas.session import MovieSession
from src.schemas.session import MovieSession as MovieSession
from src.schemas.ticket import Ticket, TicketCreate, TicketPublic
from src.schemas.user import User, UserPublic

logger = get_logger(__name__)


async def _get_room_type_by_session_id(session: Session, session_id: int) -> RoomTypeEnum:
    statement = select(Room)\
        .join(MovieSession, Room.id == MovieSession.room_id)\
        .where(MovieSession.id == session_id)
    return RoomTypeEnum(session.exec(statement).first().type)


async def _get_amount_available_seats_by_session_id(session: Session, session_id: int) -> int:
    statement = select(
        Room.capacity - select(func.count(Ticket.id)
                               ).where(Ticket.session_id == session_id)
    )\
        .join(MovieSession, MovieSession.room_id == Room.id)\
        .where(MovieSession.id == session_id)

    return session.exec(statement).first()


async def _is_seat_available(session: Session, ticket: TicketCreate) -> bool:
    statement = select(Ticket)\
        .where(Ticket.session_id == ticket.session_id)\
        .where(Ticket.seat_number == ticket.seat.number)\
        .where(Ticket.seat_row == ticket.seat.row)
    return session.exec(statement).first() is None


async def is_valid_ticket_seat(session: Session, ticket: TicketCreate) -> bool:
    available_seats_amount = await _get_amount_available_seats_by_session_id(session, ticket.session_id)
    print(available_seats_amount)
    if not available_seats_amount:
        return False

    room_type = await _get_room_type_by_session_id(session, ticket.session_id)
    print(room_type)
    if room_type == RoomTypeEnum.fixed_seats \
            and not await _is_seat_available(session, ticket):
        return False

    return True


async def create_ticket(session: Session, ticket: TicketCreate, user: UserPublic) -> Ticket:
    statement = select(MovieSession)\
        .where(MovieSession.id == ticket.session_id)
    movie_session: MovieSession = session.exec(statement).first()
    room_type = await _get_room_type_by_session_id(session, ticket.session_id)
    user_id = (await get_user_by_username(
        session=session,
        username=user.username
    )).id
    db_obj = Ticket.model_validate(
        ticket,
        update=dict(
            seat_number=ticket.seat.number if room_type == RoomTypeEnum.fixed_seats else None,
            seat_row=ticket.seat.row if room_type == RoomTypeEnum.fixed_seats else None,
            movie_id=movie_session.movie_id,
            room_id=movie_session.room_id,
            price=99,
            user_id=user_id
        )
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


async def ticket_to_public(session: Session, ticket: Ticket) -> TicketPublic:
    statement = select(Ticket, MovieSession, Room, Movie, User)\
        .where(Ticket.id == ticket.id)\
        .where(Ticket.session_id == MovieSession.id)\
        .where(Ticket.room_id == Room.id)\
        .where(Ticket.movie_id == Movie.id)\
        .where(Ticket.user_id == User.id)
    _, movie_session, room, movie, user = session.exec(statement).first()
    return TicketPublic(
        user_name=user.username,
        room_name=room.name,
        movie_name=movie.name,
        price=ticket.price,
        start_time=movie_session.start_time,
        end_time=movie_session.end_time,
        seat_number=ticket.seat_number,
        seat_row=ticket.seat_row,
    )


async def get_tickets_by_user(session: Session, user: UserPublic) -> List[Ticket]:
    user_id = (await get_user_by_username(
        session=session,
        username=user.username
    )).id
    statement = select(Ticket).where(Ticket.user_id == user_id)
    tickets = session.exec(statement).all()
    return tickets
