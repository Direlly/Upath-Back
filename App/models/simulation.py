from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Simulation(Base):
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    ano_enem = Column(Integer, nullable=False)
    nota_redacao = Column(Float, nullable=False)
    nota_natureza = Column(Float, nullable=False)
    nota_humanas = Column(Float, nullable=False)
    nota_linguagens = Column(Float, nullable=False)
    nota_matematica = Column(Float, nullable=False)
    estado = Column(String(2), nullable=False)
    modalidade = Column(String(20), nullable=False)  # ampla, cota
    media_usuario = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, nullable=False)
    curso = Column(String(200), nullable=False)
    instituicao = Column(String(200), nullable=False)
    nota_usuario = Column(Float, nullable=False)
    nota_corte = Column(Float, nullable=False)
    chance_ingresso = Column(Float, nullable=False)
    resultado = Column(String(50), nullable=False)  # acima, abaixo, dentro
    created_at = Column(DateTime(timezone=True), server_default=func.now())