from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from auth import Base

class TesteVocacional(Base):
    __tablename__ = 'teste_vocacional'
    
    id_teste = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))
    data_realizacao = Column(Date)
    resultado_perfil = Column(String(200))
    campo = Column(String(100))
    
    # Relationships
    usuario = relationship("Usuario", back_populates="testes_vocacionais")
    respostas = relationship("Resposta", back_populates="teste")

class Pergunta(Base):
    __tablename__ = 'pergunta'
    
    id_pergunta = Column(Integer, primary_key=True, autoincrement=True)
    id_area = Column(Integer, ForeignKey('area_conhecimento.id_area'))
    texto_pergunta = Column(Text, nullable=False)
    
    # Relationships
    area_conhecimento = relationship("AreaConhecimento", back_populates="perguntas")
    respostas = relationship("Resposta", back_populates="pergunta")

class Resposta(Base):
    __tablename__ = 'resposta'
    
    id_resposta = Column(Integer, primary_key=True, autoincrement=True)
    id_teste = Column(Integer, ForeignKey('teste_vocacional.id_teste'))
    id_pergunta = Column(Integer, ForeignKey('pergunta.id_pergunta'))
    alternativa = Column(String(1))
    
    # Relationships
    teste = relationship("TesteVocacional", back_populates="respostas")
    pergunta = relationship("Pergunta", back_populates="respostas")