from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
import datetime
from auth import Base

class Curso(Base):
    __tablename__ = "cursos"
    
    id_curso = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(100), nullable=False)
    area = Column(String(50), nullable=False)  # Tecnologia, Saúde, Humanas, Exatas, etc.
    descricao = Column(Text, nullable=True)
    duracao = Column(String(50), nullable=True)  # 4 anos, 5 anos, etc.
    universidades = Column(JSON, nullable=True)  # Lista de universidades que oferecem o curso
    mercado_trabalho = Column(Text, nullable=True)
    dificuldade = Column(String(20), nullable=True)  # Baixa, Media, Alta
    nota_corte_media = Column(Float, nullable=True)  # Nota de corte média no ENEM/SISU
    salario_medio = Column(Float, nullable=True)  # Salário médio inicial
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relacionamentos
    simulacoes = relationship("SimulacaoENEM", back_populates="curso")

class TesteVocacional(Base):
    __tablename__ = "testes_vocacionais"
    
    id_teste = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    status = Column(String(20), default='em_andamento')  # em_andamento, concluido, cancelado
    data_inicio = Column(DateTime, default=datetime.datetime.utcnow)
    data_fim = Column(DateTime, nullable=True)
    respostas = Column(JSON, nullable=True)  # Array de respostas do usuário
    resultados = Column(JSON, nullable=True)  # Resultado da análise da IA
    cursos_recomendados = Column(JSON, nullable=True)  # IDs dos cursos recomendados
    
    usuario = relationship("Usuario", back_populates="testes_vocacionais")

class SimulacaoENEM(Base):
    __tablename__ = "simulacoes_enem"
    
    id_simulacao = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_curso = Column(Integer, ForeignKey('cursos.id_curso'), nullable=False)
    nota_enem = Column(Float, nullable=False)
    probabilidade_ingresso = Column(Float, nullable=False)  # 0-100%
    data_simulacao = Column(DateTime, default=datetime.datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="simulacoes_enem")
    curso = relationship("Curso", back_populates="simulacoes")

class RespostaTeste(Base):
    __tablename__ = "respostas_teste"
    
    id_resposta = Column(Integer, primary_key=True, autoincrement=True)
    id_teste = Column(Integer, ForeignKey('testes_vocacionais.id_teste'), nullable=False)
    pergunta_numero = Column(Integer, nullable=False)
    resposta = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    teste = relationship("TesteVocacional")

class PerguntaTeste(Base):
    __tablename__ = "perguntas_teste"
    
    id_pergunta = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    tipo = Column(String(20), default='multipla_escolha')  # multipla_escolha, texto_livre
    opcoes = Column(JSON, nullable=True)  # Array de opções para múltipla escolha
    ordem = Column(Integer, nullable=False)
    ativa = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.datetime.utcnow)