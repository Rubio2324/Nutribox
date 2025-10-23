"""
Schemas Pydantic para validación de datos - Hijo
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


class HijoBase(BaseModel):
    """Schema base de Hijo"""
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    fecha_nacimiento: date
    grado_escolar: Optional[str] = Field(None, max_length=50)
    colegio: Optional[str] = Field(None, max_length=150)
    observaciones: Optional[str] = None


class HijoCreate(HijoBase):
    """Schema para crear Hijo"""
    padre_id: int


class HijoUpdate(BaseModel):
    """Schema para actualizar Hijo"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    fecha_nacimiento: Optional[date] = None
    grado_escolar: Optional[str] = Field(None, max_length=50)
    colegio: Optional[str] = Field(None, max_length=150)
    observaciones: Optional[str] = None
    activo: Optional[bool] = None


class Hijo(HijoBase):
    """Schema de Hijo completo"""
    id: int
    padre_id: int
    activo: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class HijoSimple(BaseModel):
    """Schema simplificado de Hijo"""
    id: int
    nombre: str
    apellido: str
    edad: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
