"""
Módulo de modelos de dados (SQLAlchemy).
"""

from models.auth import RefreshToken, PasswordResetToken, AdminSession, AuditLog
from App.models.teste import VocationalTest, TestQuestion, SuggestedCourse
from App.models.simulacao import Simulation, SimulationResult
from App.models.curso import Course, CutoffScore, Scholarship
from App.models.notificacao import Notification

__all__ = [
    
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