from fastapi import APIRouter, status

from src.core.dependencies import SessionDep
from src.core.logger import get_logger
from src.models.session import get_public_sessions_list
from src.schemas.session import MovieSessionsPublicList

session_router = APIRouter()
logger = get_logger(__name__)


@session_router.get('/', status_code=status.HTTP_200_OK)
async def read_users(db: SessionDep) -> MovieSessionsPublicList:
    return await get_public_sessions_list(db)
