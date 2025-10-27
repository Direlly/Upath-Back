from fastapi import FastAPI
from .database import engine, Base
from .routes import auth, teste, simulador, admin, users, admin_crud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='UPath API - Back-End Unificado')

# CORS - libera acesso do React e Android
origins = [
"http://localhost:3000",
"http://127.0.0.1:3000",
"http://10.0.2.2:3000",
"*" # para testes locais, depois restrinja
]
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Rotas principais
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(teste.router)
app.include_router(simulador.router)
app.include_router(admin.router)
app.include_router(admin_crud.router)


@app.get('/')
def root():
    return {"msg": "UPath API expandida rodando com CRUD administrativo para cursos, bolsas e notas de corte."}