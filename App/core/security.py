import re
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import hmac
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import settings

# Security configurations
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
PASSWORD_SALT = "upath_password_salt_2024_secure_final"
ADMIN_PIN_SALT = "upath_admin_pin_salt_2024"

security = HTTPBearer()

def validate_password_strength(password: str) -> bool:
    """
    Valida se a senha atende aos requisitos de segurança
    """
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False
    
    checks = {
        'uppercase': r'[A-Z]',
        'lowercase': r'[a-z]', 
        'number': r'\d',
        'special': r'[!@#$%^&*(),.?":{}|<>]'
    }
    
    requirements = {
        'uppercase': settings.PASSWORD_REQUIRE_UPPERCASE,
        'lowercase': settings.PASSWORD_REQUIRE_LOWERCASE,
        'number': settings.PASSWORD_REQUIRE_NUMBER,
        'special': settings.PASSWORD_REQUIRE_SPECIAL
    }
    
    for check_name, pattern in checks.items():
        if requirements[check_name] and not re.search(pattern, password):
            return False
    
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica senha usando HMAC-SHA256
    """
    try:
        expected_hash = get_password_hash(plain_password)
        # Comparação segura contra timing attacks
        return hmac.compare_digest(expected_hash, hashed_password)
    except Exception as e:
        print(f"💥 Erro ao verificar senha: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """
    Gera hash da senha usando HMAC-SHA256 
    """
    try:
        hmac_obj = hmac.new(
            PASSWORD_SALT.encode('utf-8'),
            password.encode('utf-8'), 
            hashlib.sha256
        )
        return hmac_obj.hexdigest()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar hash: {str(e)}"
        )

def criar_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token JWT
    """
    try:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
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
            JWT_SECRET, 
            algorithms=[JWT_ALGORITHM]
        )
        
        email = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role", "student")
        
        if email is None or user_id is None:
            raise credentials_exception
        
        return {"email": email, "user_id": user_id, "role": role}
        
    except JWTError:
        raise credentials_exception

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Obtém administrador do token JWT (deve ter role 'admin')
    """
    user = get_current_user(credentials)
    
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Permissão de administrador necessária."
        )
    
    return user

def validate_admin_pin(pin: str) -> bool:
    """
    Valida PIN do administrador (4 dígitos numéricos)
    """
    if len(pin) != settings.ADMIN_PIN_LENGTH or not pin.isdigit():
        return False
    return True

def get_admin_pin_hash(pin: str) -> str:
    """
    Gera hash do PIN do administrador
    """
    try:
        hmac_obj = hmac.new(
            ADMIN_PIN_SALT.encode('utf-8'),
            pin.encode('utf-8'), 
            hashlib.sha256
        )
        return hmac_obj.hexdigest()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao gerar hash do PIN: {str(e)}"
        )

# Funções auxiliares
def criar_token_recuperacao_senha(email: str) -> str:
    data = {"sub": email, "type": "password_reset"}
    return criar_token(data, timedelta(minutes=15))

def criar_token_confirmacao_email(email: str) -> str:
    data = {"sub": email, "type": "email_confirmation"}
    return criar_token(data, timedelta(hours=24))

def criar_token_admin_auth(admin_id: str) -> str:
    data = {"sub": admin_id, "type": "admin_auth", "role": "admin"}
    return criar_token(data, timedelta(minutes=10))