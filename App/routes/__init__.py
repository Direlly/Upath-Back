"""
Módulo de rotas da API FastAPI.
"""

from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.tests import router as tests_router
from routes.simulations import router as simulations_router
from routes.courses import router as courses_router
from routes.notifications import router as notifications_router
from routes.admin import router as admin_router
from routes.ia import router as ia_router

__all__ = [
    "auth_router",
    "users_router", 
    "tests_router",
    "simulations_router",
    "courses_router",
    "notifications_router", 
    "admin_router",
    "ia_router"
]