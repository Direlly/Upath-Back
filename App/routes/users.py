from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from schemas.user import UserProfileUpdate, PasswordUpdate
from services.user_service import UserService

router = APIRouter()

# Rota para obter dados da página inicial do usuário
@router.get("/home")
async def get_user_home(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    home_data = user_service.get_user_home_data(current_user["user_id"])
    
    return {
        "success": True,
        "data": home_data
    }

# Rota para obter o perfil do usuário
@router.get("/profile")
async def get_user_profile(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    profile = user_service.get_user_profile(current_user["user_id"])
    
    return {
        "success": True,
        "data": {
            "id_usuario": profile.id,
            "nome": profile.nome,
            "email": profile.email,
            "foto_url": profile.foto_url,
            "ultimo_login": profile.last_login
        }
    }

# Rota para atualizar o perfil do usuário
@router.put("/profile")
async def update_user_profile(profile_data: UserProfileUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    updated_profile = user_service.update_user_profile(current_user["user_id"], profile_data)
    
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "success": True,
        "data": {
            "mensagem": "Perfil atualizado com sucesso",
            "nome": updated_profile.nome,
            "foto_url": updated_profile.foto_url
        }
    }

# Rota para atualizar a senha do usuário
@router.put("/password")
async def update_password(password_data: PasswordUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_service = UserService(db)
    success = user_service.update_password(current_user["user_id"], password_data)
    
    if not success:
        raise HTTPException(status_code=400, detail="Senha atual incorreta")
    
    return {
        "success": True,
        "data": {
            "mensagem": "Senha atualizada com sucesso"
        }
    }

# Rota para logout do usuário
@router.post("/logout")
async def logout():
    # Em uma implementação real, invalidaríamos o token
    return {
        "success": True,
        "data": {
            "mensagem": "Logout realizado com sucesso"
        }
    }

# Rota para obter resultados de testes e simulações do usuário
@router.get("/results")
async def get_user_results(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Combinar resultados de testes e simulações
    from services.test_service import TestService
    from services.simulation_service import SimulationService
    
    test_service = TestService(db)
    simulation_service = SimulationService(db)
    
    tests = test_service.get_user_tests(current_user["user_id"])
    simulations = simulation_service.get_user_simulations(current_user["user_id"])
    
    return {
        "success": True,
        "data": {
            "testes": tests,
            "simulacoes": simulations
        }
    }