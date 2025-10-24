"""
Schemas Pydantic para validación de datos - Usuario
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# ==================== USUARIO ====================

class UsuarioBase(BaseModel):
    """Schema base de Usuario"""
    email: EmailStr
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)


class UsuarioCreate(UsuarioBase):
    """Schema para crear Usuario"""
    password: str = Field(..., min_length=6)
    rol_id: int
    tipo_membresia_id: int


class UsuarioUpdate(BaseModel):
    """Schema para actualizar Usuario"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    tipo_membresia_id: Optional[int] = None


class UsuarioChangePassword(BaseModel):
    """Schema para cambiar contraseña"""
    current_password: str
    new_password: str = Field(..., min_length=6)


class Usuario(UsuarioBase):
    """Schema de Usuario completo"""
    id: int
    activo: bool
    fecha_registro: datetime
    ultimo_acceso: Optional[datetime]
    rol_id: int
    tipo_membresia_id: int
    
    model_config = ConfigDict(from_attributes=True)


class UsuarioWithRelations(Usuario):
    """Schema de Usuario con relaciones"""
    # Usar List[dict] para evitar importaciones circulares
    hijos: List[dict] = []
    direcciones: List[dict] = []


# ==================== LOGIN ====================

class LoginRequest(BaseModel):
    """Schema para request de login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str = "bearer"
    user_info: Usuario


class TokenData(BaseModel):
    """Schema para datos del token"""
    user_id: Optional[int] = None
    email: Optional[str] = None
