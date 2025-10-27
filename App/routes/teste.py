from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from App.core.database import get_db
from models import models, schemas
from App.services.user import gerar_perfil_vocacional
from typing import List 

router = APIRouter(prefix="/teste", tags=["teste"])

@router.post('/', response_model=schemas.TesteOut)
def rodar_teste(test: schemas.TesteCreate, db: Session = Depends(get_db)):
# chama serviço de IA para gerar resultado
    resultado_text = gerar_perfil_vocacional(test.respostas)
# salvar no banco
    novo = models.TesteVocacional(respostas=str(test.respostas), resultado=str(resultado_text), user_id=None)
    db.add(novo)
    db.commit()
    db.refresh(novo)
# converter campos para retorno
    return novo