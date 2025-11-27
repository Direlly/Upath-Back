from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from core.database import engine, Base
import time

# Importar todas as rotas
from routes.auth_route import router as auth_router
from routes.admin_route import router as admin_router
from routes.perfil_route import router as perfil_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - código que roda quando a aplicação inicia
    print("🚀 Iniciando UPath API...")
    
    # Tentar criar tabelas na inicialização
    max_retries = 3
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Tabelas criadas com sucesso!")
            break
        except Exception as e:
            print(f"⚠️  Tentativa {attempt + 1}/{max_retries}: Erro ao criar tabelas: {e}")
            if attempt < max_retries - 1:
                print("🔄 Aguardando 5 segundos antes da próxima tentativa...")
                time.sleep(5)
            else:
                print("❌ Todas as tentativas falharam. A API funcionará sem banco.")
    
    yield  # A aplicação roda aqui
    
    # Shutdown - código que roda quando a aplicação para
    print("🛑 Parando UPath API...")
    # Fechar conexões do banco se necessário
    try:
        engine.dispose()
        print("✅ Conexões do banco fechadas!")
    except Exception as e:
        print(f"⚠️  Erro ao fechar conexões: {e}")

app = FastAPI(
    title="UPath API",
    description="Sistema de Orientação Vocacional e Simulação de Ingresso",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
    try:
        # Testar conexão com banco
        with engine.connect() as conn:
            conn.execute("SELECT 1") # type: ignore
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy", 
        "service": "UPath API",
        "database": db_status
    }

@app.get("/api/status")
async def api_status():
    return {
        "status": "operational",
        "version": "1.0.0",
        "services": {
            "auth": "active",
            "admin": "active", 
            "profile": "active"
        }
    }