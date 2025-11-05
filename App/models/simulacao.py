from sqlalchemy import Column, Integer, String, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Simulacao(Base):
    __tablename__ = 'simulacao'
    
    id_simulacao = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    ano_enem = Column(Integer)  # Year type mapped to Integer
    redacao = Column(DECIMAL(5, 2))
    ciencias_natureza = Column(DECIMAL(5, 2))
    ciencias_humanas = Column(DECIMAL(5, 2))
    linguagens = Column(DECIMAL(5, 2))
    matematica = Column(DECIMAL(5, 2))
    estado = Column(String(2))
    modalidade = Column(Enum('ampla', 'cotas', name='modalidade_simulacao_enum'))
    resultado_percentual = Column(DECIMAL(5, 2))
    
    # Relationships
    usuario = relationship("Usuario", back_populates="simulacoes")
    cursos_simulados = relationship("SimulacaoCurso", back_populates="simulacao")

class SimulacaoCurso(Base):
    __tablename__ = 'simulacao_curso'
    
    id_simulacao = Column(Integer, ForeignKey('simulacao.id_simulacao'), primary_key=True)
    id_curso = Column(Integer, ForeignKey('curso.id_curso'), primary_key=True)
    chance_ingresso = Column(DECIMAL(5, 2))
    
    # Relationships
    simulacao = relationship("Simulacao", back_populates="cursos_simulados")
    curso = relationship("Curso", back_populates="simulacoes_cursos")