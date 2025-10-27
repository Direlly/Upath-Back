from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from .. import models
import schemas

router = APIRouter(prefix="/admin/crud", tags=["admin-crud"])

# Reusar verificação de admin
def verificar_admin(user):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")

# -------- Cursos --------
@router.post('/cursos', response_model=schemas.CursoOut)
def criar_curso(curso_in: schemas.CursoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    curso = models.Curso(nome=curso_in.nome, area=curso_in.area, instituicao=curso_in.instituicao, descricao=curso_in.descricao)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

@router.get('/cursos', response_model=list[schemas.CursoOut])
def listar_cursos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    return db.query(models.Curso).all()

@router.get('/cursos/{curso_id}', response_model=schemas.CursoOut)
def obter_curso(curso_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.put('/cursos/{curso_id}', response_model=schemas.CursoOut)
def atualizar_curso(curso_id: int, curso_in: schemas.CursoCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    curso.nome = curso_in.nome
    curso.area = curso_in.area
    curso.instituicao = curso_in.instituicao
    curso.descricao = curso_in.descricao
    db.commit()
    db.refresh(curso)
    return curso

@router.delete('/cursos/{curso_id}')
def deletar_curso(curso_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    return {"msg": "Curso deletado"}

@router.post('/bolsas', response_model=schemas.BolsaOut)
def criar_bolsa(bolsa_in: schemas.BolsaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
# validar curso
    curso = db.query(models.Curso).filter(models.Curso.id == bolsa_in.curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    bolsa = models.Bolsa(curso_id=bolsa_in.curso_id, tipo=bolsa_in.tipo, percentual=bolsa_in.percentual, descricao=bolsa_in.descricao)
    db.add(bolsa)
    db.commit()
    db.refresh(bolsa)
    return bolsa

@router.get('/bolsas', response_model=list[schemas.BolsaOut])
def listar_bolsas(db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    return db.query(models.Bolsa).all()

@router.put('/bolsas/{bolsa_id}', response_model=schemas.BolsaOut)
def atualizar_bolsa(bolsa_id: int, bolsa_in: schemas.BolsaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    bolsa = db.query(models.Bolsa).filter(models.Bolsa.id == bolsa_id).first()
    if not bolsa:
        raise HTTPException(status_code=404, detail="Bolsa não encontrada")
    bolsa.tipo = bolsa_in.tipo
    bolsa.percentual = bolsa_in.percentual
    bolsa.descricao = bolsa_in.descricao
    bolsa.curso_id = bolsa_in.curso_id
    db.commit()
    db.refresh(bolsa)
    return bolsa

@router.delete('/bolsas/{bolsa_id}')
def deletar_bolsa(bolsa_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    bolsa = db.query(models.Bolsa).filter(models.Bolsa.id == bolsa_id).first()
    if not bolsa:
        raise HTTPException(status_code=404, detail="Bolsa não encontrada")
    db.delete(bolsa)
    db.commit()
    return {"msg": "Bolsa deletada"}

@router.post('/notas', response_model=schemas.NotaCorteOut)
def criar_nota(nota_in: schemas.NotaCorteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    curso = db.query(models.Curso).filter(models.Curso.id == nota_in.curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    nota = models.NotaCorte(curso_id=nota_in.curso_id, ano=nota_in.ano, modalidade=nota_in.modalidade, nota=nota_in.nota)
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return nota

@router.get('/notas', response_model=list[schemas.NotaCorteOut])
def listar_notas(db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    return db.query(models.NotaCorte).all()

@router.put('/notas/{nota_id}', response_model=schemas.NotaCorteOut)
def atualizar_nota(nota_id: int, nota_in: schemas.NotaCorteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    nota = db.query(models.NotaCorte).filter(models.NotaCorte.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    nota.curso_id = nota_in.curso_id
    nota.ano = nota_in.ano
    nota.modalidade = nota_in.modalidade
    nota.nota = nota_in.nota
    db.commit()
    db.refresh(nota)
    return nota

@router.delete('/notas/{nota_id}')
def deletar_nota(nota_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    verificar_admin(user)
    nota = db.query(models.NotaCorte).filter(models.NotaCorte.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    db.delete(nota)
    db.commit()
    return {"msg": "Nota deletada"}