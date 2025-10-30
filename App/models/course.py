from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from core.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    area = Column(String(100), nullable=False)
    instituicao = Column(String(200), nullable=False)
    estado = Column(String(2), nullable=False)
    duracao_anos = Column(Integer, nullable=False)
    valor = Column(Float, default=0.0)
    tipo_instituicao = Column(String(20), default="publica")  # publica, privada
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CutoffScore(Base):
    __tablename__ = "cutoff_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    curso_id = Column(Integer, nullable=False)
    instituicao = Column(String(200), nullable=False)
    nome_curso = Column(String(200), nullable=False)
    estado = Column(String(2), nullable=False)
    modalidade = Column(String(20), nullable=False)
    ano = Column(Integer, nullable=False)
    nota_corte = Column(Float, nullable=False)
    updated_by = Column(String(100), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class Scholarship(Base):
    __tablename__ = "scholarships"
    
    id = Column(Integer, primary_key=True, index=True)
    curso_id = Column(Integer, nullable=False)
    programa = Column(String(100), nullable=False)  # PROUNI, FIES, etc.
    percentual_desconto = Column(Integer, nullable=False)  # 50, 100
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())