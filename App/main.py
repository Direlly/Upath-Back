from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.core.config import settings
from app.core.database import engine, Base
from app.routes import (
    auth, users, tests, simulations, 
    courses, notifications, admin, ia
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="UPath API",
    description="Sistema de Orientação Vocacional e Simulação de Ingresso",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8081"],  # React e Mobile
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/user", tags=["Usuário"])
app.include_router(tests.router, prefix="/api/test", tags=["Testes Vocacionais"])
app.include_router(simulations.router, prefix="/api/simulation", tags=["Simulações"])
app.include_router(courses.router, prefix="/api/courses", tags=["Cursos"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notificações"])
app.include_router(admin.router, prefix="/api/admin", tags=["Administração"])
app.include_router(ia.router, prefix="/api/ia", tags=["Inteligência Artificial"])

@app.get("/")
async def root():
    return {"message": "UPath API - Sistema de Orientação Vocacional"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "UPath API"}