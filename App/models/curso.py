from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import relationship
from core.database import Base

class AreaConhecimento(Base):
    __tablename__ = 'area_conhecimento'
    
    id_area = Column(Integer, primary_key=True, autoincrement=True)
    nome_area = Column(String(100), nullable=False)
    
    # Relationships
    perguntas = relationship("Pergunta", back_populates="area_conhecimento")
    cursos = relationship("Curso", back_populates="area_rel")

class Curso(Base):
    __tablename__ = 'curso'
    
    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    area = Column(String(150))
    duracao = Column(Integer)
    instituicao = Column(String(200))
    
    # Relationships
    notas_corte = relationship("NotaCorte", back_populates="curso")
    simulacoes_cursos = relationship("SimulacaoCurso", back_populates="curso")
    area_rel = relationship("AreaConhecimento", back_populates="cursos")

class NotaCorte(Base):
    __tablename__ = 'nota_corte'
    
    id_nota = Column(Integer, primary_key=True, autoincrement=True)
    id_curso = Column(Integer, ForeignKey('curso.id_curso'))
    ano = Column(Integer)  
    estado = Column(String(2))
    modalidade = Column(Enum('ampla', 'cotas', name='modalidade_enum'))
    valor_nota = Column(DECIMAL(6, 2))
    
    # Relationships
    curso = relationship("Curso", back_populates="notas_corte")