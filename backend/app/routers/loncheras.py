"""
Router de Loncheras
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database.connection import get_db
from app.schemas.lonchera import (
    Lonchera, LoncheraCreate, LoncheraUpdate, 
    LoncheraWithAlimentos, LoncheraAlimentoCreate,
    ResumenNutricional
)
from app.services.lonchera_service import LoncheraService
from app.routers.auth import get_current_user
from app.models.models import Usuario, TipoMembresiaEnum

router = APIRouter()


def verificar_permisos_membresia(
    current_user: Usuario,
    requiere_premium: bool = False,
    requiere_estandar_o_premium: bool = False
):
    """Verificar permisos según membresía"""
    membresia = current_user.tipo_membresia.nombre
    
    if requiere_premium and membresia != TipoMembresiaEnum.PREMIUM.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta funcionalidad requiere membresía Premium"
        )
    
    if requiere_estandar_o_premium and membresia == TipoMembresiaEnum.BASICO.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta funcionalidad requiere membresía Estándar o Premium"
        )


@router.get("/", response_model=List[Lonchera])
async def listar_loncheras(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    hijo_id: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar loncheras del usuario actual
    """
    loncheras = LoncheraService.get_all(
        db,
        skip=skip,
        limit=limit,
        hijo_id=hijo_id,
        estado=estado
    )
    
    # Filtrar solo las loncheras de los hijos del usuario
    loncheras_filtradas = [
        l for l in loncheras 
        if any(h.id == l.hijo_id for h in current_user.hijos)
    ]
    
    return loncheras_filtradas


@router.get("/{lonchera_id}", response_model=LoncheraWithAlimentos)
async def obtener_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener una lonchera por ID con sus alimentos
    """
    lonchera = LoncheraService.get_by_id(db, lonchera_id=lonchera_id)
    
    if not lonchera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lonchera no encontrada"
        )
    
    # Verificar permisos
    if not any(h.id == lonchera.hijo_id for h in current_user.hijos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver esta lonchera"
        )
    
    # Calcular resumen nutricional
    resumen = LoncheraService.calcular_resumen_nutricional(db, lonchera_id)
    
    # Preparar respuesta con alimentos
    alimentos_detalle = []
    for la in lonchera.alimentos:
        alimento_info = {
            "id": la.alimento.id,
            "nombre": la.alimento.nombre,
            "tipo": la.alimento.tipo,
            "cantidad": la.cantidad,
            "calorias": la.alimento.calorias,
            "proteinas": la.alimento.proteinas,
            "carbohidratos": la.alimento.carbohidratos,
            "notas": la.notas
        }
        alimentos_detalle.append(alimento_info)
    
    response = lonchera.__dict__.copy()
    response["alimentos"] = alimentos_detalle
    response["resumen_nutricional"] = resumen.model_dump()
    
    return response


@router.post("/", response_model=Lonchera, status_code=status.HTTP_201_CREATED)
async def crear_lonchera(
    lonchera: LoncheraCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear nueva lonchera (Estándar y Premium)
    """
    verificar_permisos_membresia(current_user, requiere_estandar_o_premium=True)
    
    return LoncheraService.create(
        db,
        lonchera=lonchera,
        usuario_id=current_user.id
    )


@router.put("/{lonchera_id}", response_model=Lonchera)
async def actualizar_lonchera(
    lonchera_id: int,
    lonchera: LoncheraUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar lonchera
    """
    return LoncheraService.update(
        db,
        lonchera_id=lonchera_id,
        lonchera_update=lonchera,
        usuario_id=current_user.id
    )


@router.delete("/{lonchera_id}")
async def eliminar_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Eliminar lonchera
    """
    LoncheraService.delete(db, lonchera_id=lonchera_id, usuario_id=current_user.id)
    return {"message": "Lonchera eliminada exitosamente"}


@router.post("/{lonchera_id}/alimentos", status_code=status.HTTP_201_CREATED)
async def agregar_alimento_a_lonchera(
    lonchera_id: int,
    alimento: LoncheraAlimentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Agregar alimento a lonchera (Premium para personalización)
    """
    verificar_permisos_membresia(current_user, requiere_premium=True)
    
    return LoncheraService.agregar_alimento(
        db,
        lonchera_id=lonchera_id,
        alimento_data=alimento
    )


@router.delete("/{lonchera_id}/alimentos/{alimento_id}")
async def eliminar_alimento_de_lonchera(
    lonchera_id: int,
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Eliminar alimento de lonchera (Premium)
    """
    verificar_permisos_membresia(current_user, requiere_premium=True)
    
    LoncheraService.eliminar_alimento(db, lonchera_id=lonchera_id, alimento_id=alimento_id)
    return {"message": "Alimento eliminado de la lonchera"}


@router.get("/{lonchera_id}/resumen", response_model=ResumenNutricional)
async def obtener_resumen_nutricional(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener resumen nutricional de una lonchera
    """
    lonchera = LoncheraService.get_by_id(db, lonchera_id=lonchera_id)
    
    if not lonchera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lonchera no encontrada"
        )
    
    # Verificar permisos
    if not any(h.id == lonchera.hijo_id for h in current_user.hijos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver esta lonchera"
        )
    
    return LoncheraService.calcular_resumen_nutricional(db, lonchera_id)


@router.post("/{lonchera_id}/confirmar", response_model=Lonchera)
async def confirmar_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Confirmar lonchera (cambiar estado a confirmada)
    """
    return LoncheraService.confirmar(
        db,
        lonchera_id=lonchera_id,
        usuario_id=current_user.id
    )


@router.get("/hijo/{hijo_id}/fecha/{fecha}", response_model=LoncheraWithAlimentos)
async def obtener_lonchera_por_fecha(
    hijo_id: int,
    fecha: date,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener lonchera de un hijo en una fecha específica
    """
    # Verificar que el hijo pertenece al usuario
    if not any(h.id == hijo_id for h in current_user.hijos):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver loncheras de este hijo"
        )
    
    lonchera = LoncheraService.get_por_fecha(db, hijo_id=hijo_id, fecha=fecha)
    
    if not lonchera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay lonchera asignada para esta fecha"
        )
    
    # Calcular resumen nutricional
    resumen = LoncheraService.calcular_resumen_nutricional(db, lonchera.id)
    
    # Preparar respuesta con alimentos
    alimentos_detalle = []
    for la in lonchera.alimentos:
        alimento_info = {
            "id": la.alimento.id,
            "nombre": la.alimento.nombre,
            "tipo": la.alimento.tipo,
            "cantidad": la.cantidad,
            "calorias": la.alimento.calorias,
            "proteinas": la.alimento.proteinas,
            "carbohidratos": la.alimento.carbohidratos,
            "notas": la.notas
        }
        alimentos_detalle.append(alimento_info)
    
    response = lonchera.__dict__.copy()
    response["alimentos"] = alimentos_detalle
    response["resumen_nutricional"] = resumen.model_dump()
    
    return response
