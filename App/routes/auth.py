from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import models
from db.base import get_db
from services.email import enviar_email_recuperacao
from core.security import get_password_hash, verify_password, create_access_token
import requests
import schemas

router = APIRouter(prefix="/auth", tags=["auth"])   

@router.post('/register', response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
# verifica se email existe
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    user = models.User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
)
    db.add(user)    
    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=schemas.Token)
def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get('email')
    password = payload.get('password')
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Credenciais inválidas')
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}

# ---------------- LOGIN GOOGLE ----------------
@router.post('/google')
def login_google(payload: dict, db: Session = Depends(get_db)):
    token_google = payload.get('token')
    if not token_google:
        raise HTTPException(status_code=400, detail="Token Google não fornecido")

    resp = requests.get(f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={token_google}")
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Token Google inválido")

    data = resp.json()
    email = data['email']
    name = data.get('name', 'Usuário Google')

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(name=name, email=email, hashed_password=get_password_hash(email))
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}


# ---------------- RECUPERAÇÃO DE SENHA ----------------
@router.post('/forgot')
def forgot_password(payload: dict, db: Session = Depends(get_db)):
    email = payload.get('email')
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    token = create_access_token(user.email)
    enviar_email_recuperacao(email, token)
    return {"msg": "E-mail de recuperação enviado"}

@router.post('/reset')
def reset_password(payload: dict, db: Session = Depends(get_db)):
    token = payload.get('token')
    nova_senha = payload.get('nova_senha')
    from core.security import decode_access_token
    dados = decode_access_token(token)
    if not dados:
        return {"msg": "Senha alterada com sucesso"}