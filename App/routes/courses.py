from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from App.schemas.curso import CourseResponse
from services.course_service import CourseService

router = APIRouter()

# Rota para obter todos os cursos com filtros e paginação
@router.get("/", response_model=dict)
async def get_courses(
    q: str = Query(None, description="Termo de busca"),
    estado: str = Query(None, description="Estado filtro"),
    area: str = Query(None, description="Área filtro"),
    page: int = Query(1, description="Página"),
    db: Session = Depends(get_db)
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
    
    # Paginação simples
    per_page = 20
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_courses = courses[start_idx:end_idx]
    
    return {
        "success": True,
        "data": paginated_courses,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(courses),
            "total_pages": (len(courses) + per_page - 1) // per_page
        }
    }

# Rota para obter detalhes de um curso específico por ID
@router.get("/{course_id}", response_model=dict)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course_service = CourseService(db)
    course = course_service.get_course_by_id(course_id)
    
    if not course:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    return {
        "success": True,
        "data": course
    }