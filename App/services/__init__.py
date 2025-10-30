"""
Módulo de serviços contendo a lógica de negócio do sistema.
"""

from services.auth_service import AuthService
from services.user_service import UserService
from services.test_service import TestService
from services.simulation_service import SimulationService
from services.course_service import CourseService
from services.notification_service import NotificationService
from services.ia_service import IAService
from services.email_service import EmailService

__all__ = [
    "AuthService",
    "UserService",
    "TestService", 
    "SimulationService",
    "CourseService",
    "NotificationService",
    "IAService",
    "EmailService"
]