"""Semptify55 - API Routers"""

from app.api.cases import router as cases_router
from app.api.documents import router as documents_router
from app.api.tidbits import router as tidbits_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router

__all__ = [
    "cases_router",
    "documents_router", 
    "tidbits_router",
    "users_router",
    "auth_router",
]
