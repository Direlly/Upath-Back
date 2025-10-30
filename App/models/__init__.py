"""
Módulo de modelos de dados (SQLAlchemy).
"""

from models.user import User, UserNotificationSettings
from models.test import VocationalTest, TestQuestion, SuggestedCourse
from models.simulation import Simulation, SimulationResult
from models.course import Course, CutoffScore, Scholarship
from models.notification import Notification

__all__ = [
    "User",
    "UserNotificationSettings", 
    "VocationalTest",
    "TestQuestion",
    "SuggestedCourse", 
    "Simulation",
    "SimulationResult",
    "Course",
    "CutoffScore", 
    "Scholarship",
    "Notification"
]