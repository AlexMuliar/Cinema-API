from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel import select

from src.core.dependencies import SessionDep, TokenDep
from src.models.ticket import (create_ticket, get_tickets_by_user,
                               is_valid_ticket_seat, ticket_to_public)
from src.schemas.ticket import TicketCreate, TicketPublic, TicketPublicList
from src.schemas.user import UserPublic
from src.utils.auth import get_current_viewer_user

ticket_router = APIRouter()


@ticket_router.post(
    '/buy',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_viewer_user)],
)
async def buy_ticket(
    current_viewer_user: Annotated[UserPublic, Depends(get_current_viewer_user)],
    db: SessionDep,
    tiket: Annotated[TicketCreate, Depends()],
):
    if not await is_valid_ticket_seat(db, tiket):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat is not available",
        )
    ticket = await create_ticket(
        session=db,
        ticket=tiket,
        user=current_viewer_user,
    )
    return await ticket_to_public(db, ticket)


@ticket_router.get(
    '/my',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_viewer_user)],
    response_model=TicketPublicList,
)
async def get_user_tickets(
    current_viewer_user: Annotated[UserPublic, Depends(get_current_viewer_user)],
    db: SessionDep,
) -> TicketPublicList:
    user_tickets = await get_tickets_by_user(db, current_viewer_user)
    return TicketPublicList(
        tickets=[await ticket_to_public(db, ticket) for ticket in user_tickets]
    )
