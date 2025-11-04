from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from models.auth import Base, Usuario, Perfil
from models.curso import AreaConhecimento, Curso, NotaCorte
from models.notificacao import Notificacao, Relatorio
from models.simulacao import Simulacao, SimulacaoCurso
from models.teste import TesteVocacional, Pergunta, Resposta

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()