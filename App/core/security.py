from datetime import datetime, timedelta
from typing import Optional
import hashlib
import hmac
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = "upath_jwt_secret_2024_secure_key_final_version"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
PASSWORD_SALT = "upath_password_salt_2024_secure_final"

security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica senha usando HMAC-SHA256
    """
    try:
        print(f"🔐 Verificando senha...")
        print(f"Senha plain: {plain_password}")
        print(f"Hash esperado: {hashed_password}")
        
        expected_hash = get_password_hash(plain_password)
        print(f"Hash calculado: {expected_hash}")
        
        # Comparação segura contra timing attacks
        resultado = hmac.compare_digest(expected_hash, hashed_password)
        print(f"✅ Senha verificada: {resultado}")
        
        return resultado
    except Exception as e:
        print(f"💥 Erro ao verificar senha: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """
    Gera hash da senha usando HMAC-SHA256 
    """
    try:
        # Método robusto e sem dependências externas
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

# Funções auxiliares
def criar_token_recuperacao_senha(email: str) -> str:
    data = {"sub": email, "type": "password_reset"}
    return criar_token(data, timedelta(minutes=15))

def criar_token_confirmacao_email(email: str) -> str:
    data = {"sub": email, "type": "email_confirmation"}
    return criar_token(data, timedelta(hours=24))