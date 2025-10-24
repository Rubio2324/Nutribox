"""
Schemas Pydantic para validación de datos - Lonchera
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


class LoncheraAlimentoBase(BaseModel):
    """Schema base de Lonchera-Alimento"""
    alimento_id: int
    cantidad: int = Field(default=1, ge=1)
    notas: Optional[str] = None


class LoncheraAlimentoCreate(LoncheraAlimentoBase):
    """Schema para agregar alimento a lonchera"""
    pass


class LoncheraAlimento(LoncheraAlimentoBase):
    """Schema de Lonchera-Alimento completo"""
    id: int
    lonchera_id: int
    
    model_config = ConfigDict(from_attributes=True)


class LoncheraBase(BaseModel):
    """Schema base de Lonchera"""
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    fecha_asignacion: date


class LoncheraCreate(LoncheraBase):
    """Schema para crear Lonchera"""
    hijo_id: int
    alimentos: List[LoncheraAlimentoCreate] = []


class LoncheraUpdate(BaseModel):
    """Schema para actualizar Lonchera"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    fecha_asignacion: Optional[date] = None
    estado: Optional[str] = None


class Lonchera(LoncheraBase):
    """Schema de Lonchera completo"""
    id: int
    hijo_id: int
    estado: str
    es_predeterminada: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)


class LoncheraWithAlimentos(Lonchera):
    """Schema de Lonchera con alimentos"""
    # Simplemente, usa List[dict], ya lo tenías bien
    alimentos: List[dict] = []
    resumen_nutricional: Optional[dict] = None


class LoncheraSimple(BaseModel):
    """Schema simplificado de Lonchera"""
    id: int
    nombre: str
    fecha_asignacion: date
    estado: str
    
    model_config = ConfigDict(from_attributes=True)


class ResumenNutricional(BaseModel):
    """Schema para resumen nutricional de lonchera"""
    total_calorias: float = 0.0
    total_proteinas: float = 0.0
    total_carbohidratos: float = 0.0
    total_grasas: float = 0.0
    total_fibra: float = 0.0
    num_alimentos: int = 0
