from fastapi import FastAPI

from src.routes.admin import admin_router
from src.routes.auth import auth_router
from src.routes.session import session_router
from src.routes.ticket import ticket_router
from src.routes.user import user_router

app = FastAPI()
app.include_router(auth_router, prefix='/oauth')
app.include_router(user_router, prefix='/user')
app.include_router(session_router, prefix='/session')
app.include_router(ticket_router, prefix='/ticket')
app.include_router(admin_router, prefix='/admin')


app.get('/health', status_code=200)


def health() -> dict:
    return {'version': '0.0.1'}
