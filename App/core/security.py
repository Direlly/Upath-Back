from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from core.config import settings

# Configuração do passlib para hashing seguro
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica senha usando bcrypt
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Erro ao verificar senha: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """
    Gera hash da senha usando bcrypt
    """
    return pwd_context.hash(password)

def criar_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token JWT
    """
    try:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar token: {str(e)}"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Obtém usuário do token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        email = payload.get("sub")
        user_id = payload.get("user_id")
        role = payload.get("role", "student")
        username = payload.get("username")
        name = payload.get("name")
        
        if email is None or user_id is None:
            raise credentials_exception
        
        return {
            "email": email, 
            "user_id": user_id, 
            "role": role,
            "username": username,
            "name": name
        }
        
    except JWTError:
        raise credentials_exception

def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Verifica se o usuário atual é admin
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado - requer privilégios de administrador"
        )
    return current_user

# Funções auxiliares para compatibilidade
def criar_token_recuperacao_senha() -> str:
    """
    Gera token aleatório para recuperação de senha
    """
    import secrets
    import string
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(32))