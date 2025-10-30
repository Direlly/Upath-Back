from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text
from sqlalchemy.sql import func
from core.database import Base

class VocationalTest(Base):
    __tablename__ = "vocational_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    test_name = Column(String(100), nullable=False)
    mode = Column(String(20), default="gratuito")  # gratuito, pago
    status = Column(String(20), default="in_progress")  # in_progress, completed
    area_conhecimento = Column(String(100), nullable=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class TestQuestion(Base):
    __tablename__ = "test_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    question_order = Column(Integer, nullable=False)
    answer = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SuggestedCourse(Base):
    __tablename__ = "suggested_courses"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=True)
    course_name = Column(String(200), nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())