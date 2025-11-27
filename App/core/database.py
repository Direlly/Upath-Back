from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Log da URL de conexão (com senha mascarada para segurança)
try:
    url_parts = settings.DATABASE_URL.split('://')
    if len(url_parts) > 1:
        credentials = url_parts[1].split('@')[0]
        if ':' in credentials:
            password = credentials.split(':')[1]
            masked_url = settings.DATABASE_URL.replace(password, '***')
        else:
            masked_url = settings.DATABASE_URL
    else:
        masked_url = settings.DATABASE_URL
except:
    masked_url = settings.DATABASE_URL

logger.info(f"🔗 Tentando conectar com: {masked_url}")

Base = declarative_base()

try:
    # Criar engine com configurações robustas
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=True,
        pool_recycle=3600,
        connect_args={
            "connect_timeout": 10
        }
    )
    
    # Testar conexão imediatamente
    logger.info("🧪 Testando conexão com banco...")
    with engine.connect() as conn:
        # Teste básico
        result = conn.execute(text("SELECT 1"))
        logger.info("✅ Teste SELECT 1: OK")
        
        # Informações do banco
        db_info = conn.execute(text("SELECT DATABASE(), USER(), VERSION()"))
        info_data = db_info.fetchone()
        if info_data:
            logger.info(f"📊 Banco: {info_data[0]}, Usuário: {info_data[1]}, Versão: {info_data[2]}")
        else:
            logger.warning("⚠️ Não foi possível obter informações do banco")
        
        # Listar tabelas
        tables_result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in tables_result.fetchall()] if tables_result else []
        logger.info(f"📋 Tabelas existentes: {tables}")
    
    logger.info("🎉 Conexão com banco estabelecida com sucesso!")
    
except Exception as e:
    logger.error(f"💥 ERRO CRÍTICO na conexão com banco: {e}")
    logger.error("💡 Possíveis soluções:")
    logger.error("   1. Verifique se o MySQL está rodando")
    logger.error("   2. Verifique se a senha está correta") 
    logger.error("   3. Verifique se o banco 'upath_db' existe")
    logger.error("   4. Verifique se o usuário tem privilégios")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    try:
        logger.info("🏗️ Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tabelas criadas/verificadas com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        raise
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"❌ Erro na sessão do banco: {e}")
        db.rollback()
        raise
    finally:
        db.close()