"""
Schemas Pydantic para validación de datos - Alimento
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class AlimentoBase(BaseModel):
    """Schema base de Alimento"""
    nombre: str = Field(..., min_length=2, max_length=100)
    tipo: str = Field(..., max_length=50)
    descripcion: Optional[str] = None
    calorias: float = Field(..., ge=0)
    proteinas: float = Field(..., ge=0)
    carbohidratos: float = Field(..., ge=0)
    grasas: float = Field(default=0.0, ge=0)
    fibra: float = Field(default=0.0, ge=0)
    imagen_url: Optional[str] = None


class AlimentoCreate(AlimentoBase):
    """Schema para crear Alimento"""
    pass


class AlimentoUpdate(BaseModel):
    """Schema para actualizar Alimento"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    tipo: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    calorias: Optional[float] = Field(None, ge=0)
    proteinas: Optional[float] = Field(None, ge=0)
    carbohidratos: Optional[float] = Field(None, ge=0)
    grasas: Optional[float] = Field(None, ge=0)
    fibra: Optional[float] = Field(None, ge=0)
    imagen_url: Optional[str] = None
    estado: Optional[str] = None


class Alimento(AlimentoBase):
    """Schema de Alimento completo"""
    id: int
    estado: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


class AlimentoSimple(BaseModel):
    """Schema simplificado de Alimento"""
    id: int
    nombre: str
    tipo: str
    calorias: float
    estado: str
    
    model_config = ConfigDict(from_attributes=True)


class AlimentoNutricional(BaseModel):
    """Schema para información nutricional"""
    id: int
    nombre: str
    calorias: float
    proteinas: float
    carbohidratos: float
    grasas: float
    fibra: float
    
    model_config = ConfigDict(from_attributes=True)
