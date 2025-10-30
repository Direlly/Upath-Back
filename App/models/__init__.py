"""
Módulo de modelos de dados (SQLAlchemy).
"""

from models.user import User, UserNotificationSettings
from models.auth import RefreshToken, PasswordResetToken, AdminSession, AuditLog
from models.test import VocationalTest, TestQuestion, SuggestedCourse
from models.simulation import Simulation, SimulationResult
from models.course import Course, CutoffScore, Scholarship
from models.notification import Notification

__all__ = [
    # User models
    "User",
    "UserNotificationSettings",
    
    # Auth models
    "RefreshToken",
    "PasswordResetToken", 
    "AdminSession",
    "AuditLog",
    
    # Test models
    "VocationalTest",
    "TestQuestion",
    "SuggestedCourse", 
    
    # Simulation models
    "Simulation",
    "SimulationResult",
    
    # Course models
    "Course",
    "CutoffScore", 
    "Scholarship",
    
    # Notification models
    "Notification"
]