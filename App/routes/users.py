from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import models
from App.core.database import get_db
import schemas

router = APIRouter(prefix="/user", tags=["user"])


@router.get('/me', response_model=schemas.UserOut)
def get_me(user=Depends(get_current_user)):
    return user

@router.put('/preferences')
def atualizar_preferencias(preferencias: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_prefs = preferencias.get('notificacoes', True)
    user_prefs_field = getattr(user, 'preferencias', None)
    user.preferencias = str(preferencias)
    db.commit()
    return {"msg": "Preferências atualizadas"}  