from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_admin
from App.schemas.curso import CourseCreate, CutoffUpdate, ScholarshipCreate
from services.course_service import CourseService
from services.email_service import EmailService
import secrets
from datetime import datetime, timedelta

router = APIRouter()

# Simulação de sessões admin temporárias para 2FA
admin_sessions = {}

# Rota para login admin e envio do PIN 2FA
@router.post("/login")
async def admin_login(credentials: dict, db: Session = Depends(get_db)):
    # Verificar credenciais (simplificado)
    if credentials.get("email") == "admin@upath.com" and credentials.get("senha") == "Admin@123":
        session_id = secrets.token_hex(16)
        pin_code = str(secrets.randbelow(10000)).zfill(4)
        
        # Salvar sessão temporária
        admin_sessions[session_id] = {
            "email": "admin@upath.com",
            "pin_code": pin_code,
            "created_at": datetime.utcnow()
        }
        
        # Enviar PIN por email
        email_service = EmailService()
        email_service.send_admin_2fa_email("admin@upath.com", pin_code)
        
        return {
            "success": True,
            "data": {
                "session_id": session_id
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

# Rota para verificar o PIN 2FA e obter token JWT
@router.post("/verify-pin")
async def admin_verify_2fa(verification_data: dict):
    session_id = verification_data.get("session_id")
    token_4d = verification_data.get("token_4d")
    
    session = admin_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    # Verificar expiração (10 minutos)
    if datetime.utcnow() - session["created_at"] > timedelta(minutes=10):
        del admin_sessions[session_id]
        raise HTTPException(status_code=401, detail="PIN expirado")
    
    if session["pin_code"] != token_4d:
        raise HTTPException(status_code=401, detail="PIN incorreto")
    
    # Gerar JWT admin
    from core.security import create_access_token
    access_token = create_access_token(
        data={
            "sub": session["email"],
            "user_id": 0,  # ID especial para admin
            "role": "admin"
        },
        expires_delta=timedelta(hours=8)
    )
    
    # Limpar sessão temporária
    del admin_sessions[session_id]
    
    return {
        "success": True,
        "data": {
            "token": access_token,
            "user": {
                "email": session["email"],
                "role": "admin"
            }
        }
    }

# Rota para atualizar nota de corte de um curso
@router.post("/notas-corte")
async def update_cutoff_score(
    cutoff_data: CutoffUpdate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    success = course_service.update_cutoff_score(cutoff_data, current_admin["email"])
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Aconteceu um erro inesperado ao enviar para o banco de dados. Tente novamente."
        )
    
    return {
        "success": True,
        "data": {
            "mensagem": "Tudo pronto, agora as simulações passam a usar os novos dados!",
            "ultima_atualizacao": datetime.utcnow().isoformat() + "Z",
            "atualizado_por": current_admin["email"]
        }
    }

# Rota para obter a última atualização de nota de corte
@router.get("/notas-corte")
async def get_last_cutoff_update(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    course_service = CourseService(db)
    last_update = course_service.get_last_cutoff_update()
    
    if not last_update:
        raise HTTPException(status_code=404, detail="Nenhuma atualização encontrada")
    
    return {
        "success": True,
        "data": {
            "nome_instituicao": last_update.instituicao,
            "nome_curso": last_update.nome_curso,
            "ano": last_update.ano,
            "modalidade": last_update.modalidade,
            "nota_corte": last_update.nota_corte,
            "data_atualizacao": last_update.updated_at.isoformat() + "Z",
            "atualizado_por": last_update.updated_by
        }
    }

# Rota para listar todos os cursos
@router.get("/cursos")
async def admin_get_courses(
    q: str = Query(None),
    estado: str = Query(None),
    area: str = Query(None),
    page: int = Query(1),
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    
    filters = {}
    if q:
        filters['q'] = q
    if estado:
        filters['estado'] = estado
    if area:
        filters['area'] = area
    
    courses = course_service.get_all_courses(filters)
    
    return {
        "success": True,
        "data": courses
    }

# Rota para criar um novo curso
@router.post("/cursos")
async def admin_create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    course = course_service.create_course(course_data)
    
    return {
        "success": True,
        "data": {
            "id_curso": course.id,
            "mensagem": "Curso salvo com sucesso."
        }
    }

# Rota para atualizar um curso existente
@router.put("/cursos/{id}")
async def admin_update_course(
    id: int,
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    course = course_service.update_course(id, course_data)
    
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    return {
        "success": True,
        "data": {
            "mensagem": "Curso atualizado com sucesso"
        }
    }

# Rota para deletar um curso
@router.delete("/cursos/{id}")
async def admin_delete_course(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    success = course_service.delete_course(id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    return {
        "success": True,
        "data": {
            "mensagem": "Curso excluído com sucesso"
        }
    }

# Rota para adicionar uma bolsa a um curso
@router.post("/cursos/{id}/bolsa")
async def admin_add_scholarship(
    id: int,
    scholarship_data: ScholarshipCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    success = course_service.add_scholarship(id, scholarship_data)

    if not success:
        raise HTTPException(status_code=400, detail="Não foi possível vincular bolsa. Verifique se o curso é de instituição privada.")
    
    return {
        "success": True,
        "data": {
            "mensagem": f"Bolsa {scholarship_data.programa} ({scholarship_data.percentual_desconto}%) vinculada ao curso com sucesso."
        }
    }

# Rota para remover uma bolsa de um curso
@router.delete("/cursos/{id}/bolsa")
async def admin_remove_scholarship(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin)
):
    course_service = CourseService(db)
    success = course_service.remove_scholarship(id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Bolsa não encontrada")
    
    return {
        "success": True,
        "data": {
            "mensagem": "Bolsa desvinculada com sucesso"
        }
    }