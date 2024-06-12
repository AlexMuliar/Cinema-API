from datetime import date

from sqlmodel import Session, and_, func, select

from src.schemas.movie import Movie
from src.schemas.session import MovieSession
from src.schemas.ticket import Ticket


async def get_report_for_data_range(*, session: Session, start_date: date, end_date: date):
    statement = select(
        Movie.name,
        func.date(MovieSession.start_time).label("day"),
        func.count(Ticket.id).label("tickets_sold"),
    ).join(Movie, Ticket.movie_id == Movie.id
           ).join(MovieSession, Ticket.session_id == MovieSession.id
                  ).where(
        and_(
            func.date(MovieSession.start_time) >= start_date,
            func.date(MovieSession.start_time) <= end_date,
        )
    ).group_by(Movie.name, func.date(MovieSession.start_time))

    return session.exec(statement).all()
