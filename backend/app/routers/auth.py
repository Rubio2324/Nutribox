"""
Router de Autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.connection import get_db
from app.schemas.usuario import LoginRequest, Token, Usuario
from app.services.usuario_service import UsuarioService
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings
from app.models.models import Usuario as UsuarioModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UsuarioModel:
    """Dependency para obtener el usuario actual del token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    usuario = UsuarioService.get_by_id(db, usuario_id=int(user_id))
    
    if usuario is None:
        raise credentials_exception
    
    return usuario


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de login
    """
    usuario = UsuarioService.authenticate(
        db,
        email=login_data.email,
        password=login_data.password
    )
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(usuario.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": usuario
    }


@router.post("/token", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login compatible con OAuth2
    """
    usuario = UsuarioService.authenticate(
        db,
        email=form_data.username,
        password=form_data.password
    )
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(usuario.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": usuario
    }


@router.get("/me", response_model=Usuario)
async def read_users_me(
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Obtener información del usuario actual
    """
    return current_user


@router.post("/logout")
async def logout(
    current_user: UsuarioModel = Depends(get_current_user)
):
    """
    Endpoint de logout (el cliente debe eliminar el token)
    """
    return {"message": "Logout exitoso"}
