"""
Módulo de schemas Pydantic para validação de dados.
"""

from schemas.user import (
    UserBase,
    UserCreate, 
    UserLogin,
    UserResponse,
    UserProfileUpdate,
    PasswordUpdate
)

from schemas.test import (
    TestStart,
    TestAnswer, 
    TestFinish,
    TestResponse,
    TestHistory
)

from schemas.simulation import (
    SimulationCreate,
    SimulationResult,
    SimulationResponse, 
    SimulationHistory
)

from schemas.course import (
    CourseBase,
    CourseCreate,
    CourseResponse,
    CutoffUpdate, 
    ScholarshipCreate
)

from schemas.notification import (
    NotificationBase,
    NotificationResponse,
    NotificationSettings
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserLogin", 
    "UserResponse",
    "UserProfileUpdate",
    "PasswordUpdate",
    
    # Test schemas
    "TestStart",
    "TestAnswer",
    "TestFinish", 
    "TestResponse",
    "TestHistory",
    
    # Simulation schemas
    "SimulationCreate", 
    "SimulationResult",
    "SimulationResponse",
    "SimulationHistory",
    
    # Course schemas
    "CourseBase",
    "CourseCreate",
    "CourseResponse", 
    "CutoffUpdate",
    "ScholarshipCreate",
    
    # Notification schemas
    "NotificationBase",
    "NotificationResponse", 
    "NotificationSettings"
]