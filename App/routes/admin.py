from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models
from db.base import get_db
from db.base import get_current_user
import schemas

router = APIRouter(prefix="/admin", tags=["admin"])

# Middleware simples de autorização
def verificar_admin(user):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")


@router.get('/usuarios', response_model=list[schemas.UserOut])
def listar_usuarios(db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    return db.query(models.User).all()


@router.delete('/usuarios/{user_id}')
def remover_usuario(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    alvo = db.query(models.User).filter(models.User.id == user_id).first()
    if not alvo:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(alvo)
    db.commit()
    return {"msg": "Usuário removido"}


@router.get('/logs')
def visualizar_logs():
# Em produção: conectar com sistema de logs real
    return {"logs": ["Login bem-sucedido de admin", "Usuário X deletado"]}