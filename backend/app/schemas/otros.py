"""
Schemas Pydantic para validación de datos - Direccion, Restriccion
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


# ==================== DIRECCION ====================

class DireccionBase(BaseModel):
    """Schema base de Direccion"""
    nombre: str = Field(..., min_length=2, max_length=100)
    direccion_linea1: str = Field(..., min_length=5, max_length=200)
    direccion_linea2: Optional[str] = Field(None, max_length=200)
    barrio: str = Field(..., max_length=100)
    ciudad: str = Field(..., max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=20)
    referencia: Optional[str] = None
    es_principal: bool = False


class DireccionCreate(DireccionBase):
    """Schema para crear Direccion"""
    usuario_id: int


class DireccionUpdate(BaseModel):
    """Schema para actualizar Direccion"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    direccion_linea1: Optional[str] = Field(None, min_length=5, max_length=200)
    direccion_linea2: Optional[str] = Field(None, max_length=200)
    barrio: Optional[str] = Field(None, max_length=100)
    ciudad: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=20)
    referencia: Optional[str] = None
    es_principal: Optional[bool] = None


class Direccion(DireccionBase):
    """Schema de Direccion completo"""
    id: int
    usuario_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DireccionSimple(BaseModel):
    """Schema simplificado de Direccion"""
    id: int
    nombre: str
    direccion_linea1: str
    ciudad: str
    
    model_config = ConfigDict(from_attributes=True)


# ==================== RESTRICCION ====================

class RestriccionBase(BaseModel):
    """Schema base de Restriccion"""
    tipo: str = Field(..., max_length=50)
    descripcion: str
    severidad: str = Field(..., max_length=20)


class RestriccionCreate(RestriccionBase):
    """Schema para crear Restriccion"""
    hijo_id: int


class RestriccionUpdate(BaseModel):
    """Schema para actualizar Restriccion"""
    tipo: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    severidad: Optional[str] = Field(None, max_length=20)
    activa: Optional[bool] = None


class Restriccion(RestriccionBase):
    """Schema de Restriccion completo"""
    id: int
    hijo_id: int
    activa: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== EXCEPCION ====================

class ExcepcionBase(BaseModel):
    """Schema base de Excepcion"""
    motivo: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    autorizado_por: Optional[str] = Field(None, max_length=100)


class ExcepcionCreate(ExcepcionBase):
    """Schema para crear Excepcion"""
    restriccion_id: int


class Excepcion(ExcepcionBase):
    """Schema de Excepcion completo"""
    id: int
    restriccion_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== ROL Y MEMBRESIA ====================

class RolBase(BaseModel):
    """Schema base de Rol"""
    nombre: str
    descripcion: Optional[str] = None


class Rol(RolBase):
    """Schema de Rol completo"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TipoMembresiaBase(BaseModel):
    """Schema base de Tipo Membresia"""
    nombre: str
    descripcion: Optional[str] = None
    max_direcciones: int = 0
    permite_personalizacion: bool = False
    permite_restricciones: bool = False
    permite_estadisticas_avanzadas: bool = False
    precio_mensual: float = 0.0


class TipoMembresia(TipoMembresiaBase):
    """Schema de Tipo Membresia completo"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
