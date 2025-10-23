"""
Router de Alimentos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.alimento import Alimento, AlimentoCreate, AlimentoUpdate, AlimentoSimple
from app.services.alimento_service import AlimentoService
from app.routers.auth import get_current_user
from app.models.models import Usuario, RolEnum

router = APIRouter()


def require_admin(current_user: Usuario = Depends(get_current_user)):
    """Dependency para requerir rol de administrador"""
    if current_user.rol.nombre != RolEnum.ADMINISTRADOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos de administrador"
        )
    return current_user


@router.get("/", response_model=List[Alimento])
async def listar_alimentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar alimentos con filtros opcionales
    """
    alimentos = AlimentoService.get_all(
        db,
        skip=skip,
        limit=limit,
        estado=estado,
        tipo=tipo
    )
    return alimentos


@router.get("/activos", response_model=List[Alimento])
async def listar_alimentos_activos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar solo alimentos activos
    """
    alimentos = AlimentoService.get_activos(db, skip=skip, limit=limit)
    return alimentos


@router.get("/buscar", response_model=List[Alimento])
async def buscar_alimentos(
    q: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Buscar alimentos por nombre o tipo
    """
    alimentos = AlimentoService.search(db, query=q, skip=skip, limit=limit)
    return alimentos


@router.get("/tipo/{tipo}", response_model=List[Alimento])
async def listar_por_tipo(
    tipo: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar alimentos por tipo
    """
    alimentos = AlimentoService.get_por_tipo(db, tipo=tipo)
    return alimentos


@router.get("/{alimento_id}", response_model=Alimento)
async def obtener_alimento(
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener un alimento por ID
    """
    alimento = AlimentoService.get_by_id(db, alimento_id=alimento_id)
    
    if not alimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alimento no encontrado"
        )
    
    return alimento


@router.post("/", response_model=Alimento, status_code=status.HTTP_201_CREATED)
async def crear_alimento(
    alimento: AlimentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Crear nuevo alimento (solo administradores)
    """
    return AlimentoService.create(db, alimento=alimento, usuario_id=current_user.id)


@router.put("/{alimento_id}", response_model=Alimento)
async def actualizar_alimento(
    alimento_id: int,
    alimento: AlimentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Actualizar alimento (solo administradores)
    """
    return AlimentoService.update(
        db,
        alimento_id=alimento_id,
        alimento_update=alimento,
        usuario_id=current_user.id
    )


@router.delete("/{alimento_id}", response_model=Alimento)
async def eliminar_alimento(
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Eliminar alimento - soft delete (solo administradores)
    """
    return AlimentoService.soft_delete(
        db,
        alimento_id=alimento_id,
        usuario_id=current_user.id
    )


@router.post("/{alimento_id}/restaurar", response_model=Alimento)
async def restaurar_alimento(
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Restaurar alimento eliminado (solo administradores)
    """
    return AlimentoService.restore(
        db,
        alimento_id=alimento_id,
        usuario_id=current_user.id
    )


@router.get("/{alimento_id}/historial")
async def obtener_historial(
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin)
):
    """
    Obtener historial de un alimento (solo administradores)
    """
    historial = AlimentoService.get_historial(db, alimento_id=alimento_id)
    return historial
