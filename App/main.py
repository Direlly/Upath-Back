from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
from core.config import settings
from core.database import engine, Base, SessionLocal
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar todas as rotas
from routes.auth_route import router as auth_router
from routes.admin_route import router as admin_router
from routes.perfil_route import router as perfil_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - código que roda quando a aplicação inicia
    logger.info("🚀 Iniciando UPath API...")
    
    # Testar conexão com banco na inicialização
    try:
        logger.info("🔍 Testando conexão com o banco de dados...")
        
        # Teste 1: Conexão básica
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Teste de conexão básica: OK")
        
        # Teste 2: Verificar se o banco existe
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE()"))
            current_db = result.scalar()
            logger.info(f"📊 Banco atual: {current_db}")
        
        # Teste 3: Listar tabelas existentes
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables_result = result.fetchall()
            tables = [row[0] for row in tables_result] if tables_result else []
            logger.info(f"📋 Tabelas existentes: {tables}")
            
        # Teste 4: Verificar versão do MySQL
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.scalar()
            logger.info(f"🐬 Versão do MySQL: {version}")
            
        logger.info("🎉 Todas as verificações de banco passaram!")
        
    except Exception as e:
        logger.error(f"❌ ERRO NA CONEXÃO COM BANCO: {e}")
        logger.error("⚠️ A aplicação continuará, mas funcionalidades de banco podem falhar")
    
    yield  # A aplicação roda aqui
    
    # Shutdown - código que roda quando a aplicação para
    logger.info("🛑 Encerrando UPath API...")
    engine.dispose()

app = FastAPI(
    title="UPath API",
    description="Sistema de Orientação Vocacional e Simulação de Ingresso",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - Corrigido para permitir todas as origens do localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(auth_router, prefix="/api", tags=["Autenticação"])
app.include_router(admin_router, prefix="/api", tags=["Administração"])
app.include_router(perfil_router, prefix="/api", tags=["Perfil"])

@app.get("/")
async def root():
    return {"message": "UPath API - Sistema de Orientação Vocacional"}

@app.get("/health")
async def health_check():
    """Endpoint de health check mais detalhado"""
    start_time = time.time()
    
    try:
        # Testar conexão com banco
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            db_status = "healthy"
            
            # Verificar informações do banco
            db_info = conn.execute(text("SELECT DATABASE(), USER(), VERSION()"))
            db_data = db_info.fetchone()
            
    except Exception as e:
        db_status = f"unhealthy - {str(e)}"
        db_data = None
    
    response_time = round((time.time() - start_time) * 1000, 2)
    
    return {
        "status": "healthy", 
        "service": "UPath API",
        "timestamp": time.time(),
        "response_time_ms": response_time,
        "database": {
            "status": db_status,
            "name": db_data[0] if db_data else "unknown",
            "user": db_data[1] if db_data else "unknown",
            "version": db_data[2] if db_data else "unknown"
        }
    }

@app.get("/api/status")
async def api_status():
    """Status detalhado da API"""
    try:
        # Testar cada módulo do banco
        db_test = {}
        with engine.connect() as conn:
            # Testar acesso a tabelas básicas
            try:
                conn.execute(text("SELECT 1 FROM users LIMIT 1"))
                db_test["users_table"] = "accessible"
            except Exception as table_error:
                db_test["users_table"] = f"inaccessible - {str(table_error)}"
                
    except Exception as e:
        db_test = {"error": str(e)}
    
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": time.time(),
        "services": {
            "auth": "active",
            "admin": "active", 
            "profile": "active"
        },
        "database_test": db_test
    }

@app.get("/api/debug/database")
async def debug_database():
    """Endpoint para debug completo do banco"""
    try:
        with engine.connect() as conn:
            # Informações da conexão
            conn_info = conn.execute(text("SELECT DATABASE(), USER(), CONNECTION_ID()"))
            conn_data = conn_info.fetchone()
            
            # Listar todas as tabelas
            tables_result = conn.execute(text("SHOW TABLES"))
            tables_data = tables_result.fetchall()
            tables = [row[0] for row in tables_data] if tables_data else []
            
            # Informações do servidor
            version_result = conn.execute(text("SELECT VERSION()"))
            version = version_result.scalar()
            
        return {
            "connection": {
                "database": conn_data[0] if conn_data else "unknown",
                "user": conn_data[1] if conn_data else "unknown",
                "connection_id": conn_data[2] if conn_data else "unknown"
            },
            "server": {
                "version": version if version else "unknown"
            },
            "tables": tables,
            "table_count": len(tables),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {str(e)}")

@app.get("/api/test-connection")
async def test_connection():
    """Endpoint simples para testar conexão com banco"""
    try:
        with engine.connect() as conn:
            # Teste rápido
            result = conn.execute(text("SELECT 1 as status, NOW() as timestamp"))
            test_data = result.fetchone()
            
        return {
            "database_connection": "success",
            "timestamp": test_data[1] if test_data else "unknown",
            "message": "Conexão com banco estabelecida com sucesso"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Falha na conexão com banco: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)