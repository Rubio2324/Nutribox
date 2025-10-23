"""
Servicio de Alimento - Lógica de negocio
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from app.models.models import Alimento, HistorialAlimento, EstadoAlimentoEnum
from app.schemas.alimento import AlimentoCreate, AlimentoUpdate
from fastapi import HTTPException, status
import json


class AlimentoService:
    """Servicio para gestión de alimentos"""
    
    @staticmethod
    def get_by_id(db: Session, alimento_id: int) -> Optional[Alimento]:
        """Obtener alimento por ID"""
        return db.query(Alimento).filter(Alimento.id == alimento_id).first()
    
    @staticmethod
    def get_all(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        estado: Optional[str] = None,
        tipo: Optional[str] = None
    ) -> List[Alimento]:
        """Obtener lista de alimentos con filtros"""
        query = db.query(Alimento)
        
        if estado:
            query = query.filter(Alimento.estado == estado)
        
        if tipo:
            query = query.filter(Alimento.tipo == tipo)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_activos(db: Session, skip: int = 0, limit: int = 100) -> List[Alimento]:
        """Obtener solo alimentos activos"""
        return AlimentoService.get_all(
            db, 
            skip=skip, 
            limit=limit, 
            estado=EstadoAlimentoEnum.ACTIVO.value
        )
    
    @staticmethod
    def create(db: Session, alimento: AlimentoCreate, usuario_id: int = None) -> Alimento:
        """Crear nuevo alimento"""
        db_alimento = Alimento(**alimento.model_dump())
        
        db.add(db_alimento)
        db.commit()
        db.refresh(db_alimento)
        
        # Registrar en historial
        AlimentoService._registrar_historial(
            db, 
            alimento_id=db_alimento.id,
            accion="Creado",
            usuario_id=usuario_id
        )
        
        return db_alimento
    
    @staticmethod
    def update(
        db: Session, 
        alimento_id: int, 
        alimento_update: AlimentoUpdate,
        usuario_id: int = None
    ) -> Alimento:
        """Actualizar alimento"""
        db_alimento = AlimentoService.get_by_id(db, alimento_id)
        
        if not db_alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado"
            )
        
        # Guardar datos anteriores
        datos_anteriores = {
            "nombre": db_alimento.nombre,
            "tipo": db_alimento.tipo,
            "calorias": db_alimento.calorias,
            "proteinas": db_alimento.proteinas,
            "carbohidratos": db_alimento.carbohidratos
        }
        
        # Actualizar campos
        update_data = alimento_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_alimento, field, value)
        
        db.commit()
        db.refresh(db_alimento)
        
        # Registrar en historial
        AlimentoService._registrar_historial(
            db,
            alimento_id=db_alimento.id,
            accion="Modificado",
            usuario_id=usuario_id,
            datos_anteriores=json.dumps(datos_anteriores)
        )
        
        return db_alimento
    
    @staticmethod
    def soft_delete(db: Session, alimento_id: int, usuario_id: int = None) -> Alimento:
        """Eliminar alimento (soft delete)"""
        db_alimento = AlimentoService.get_by_id(db, alimento_id)
        
        if not db_alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado"
            )
        
        # Guardar datos antes de eliminar
        datos_anteriores = {
            "nombre": db_alimento.nombre,
            "tipo": db_alimento.tipo,
            "estado": db_alimento.estado
        }
        
        # Cambiar estado a inactivo
        db_alimento.estado = EstadoAlimentoEnum.INACTIVO.value
        db.commit()
        db.refresh(db_alimento)
        
        # Registrar en historial
        AlimentoService._registrar_historial(
            db,
            alimento_id=db_alimento.id,
            accion="Eliminado",
            usuario_id=usuario_id,
            datos_anteriores=json.dumps(datos_anteriores)
        )
        
        return db_alimento
    
    @staticmethod
    def restore(db: Session, alimento_id: int, usuario_id: int = None) -> Alimento:
        """Restaurar alimento eliminado"""
        db_alimento = AlimentoService.get_by_id(db, alimento_id)
        
        if not db_alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado"
            )
        
        db_alimento.estado = EstadoAlimentoEnum.ACTIVO.value
        db.commit()
        db.refresh(db_alimento)
        
        # Registrar en historial
        AlimentoService._registrar_historial(
            db,
            alimento_id=db_alimento.id,
            accion="Restaurado",
            usuario_id=usuario_id
        )
        
        return db_alimento
    
    @staticmethod
    def get_historial(db: Session, alimento_id: int) -> List[HistorialAlimento]:
        """Obtener historial de un alimento"""
        return db.query(HistorialAlimento)\
            .filter(HistorialAlimento.alimento_id == alimento_id)\
            .order_by(HistorialAlimento.created_at.desc())\
            .all()
    
    @staticmethod
    def search(
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Alimento]:
        """Buscar alimentos por nombre o tipo"""
        return db.query(Alimento).filter(
            or_(
                Alimento.nombre.ilike(f"%{query}%"),
                Alimento.tipo.ilike(f"%{query}%")
            ),
            Alimento.estado == EstadoAlimentoEnum.ACTIVO.value
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_por_tipo(db: Session, tipo: str) -> List[Alimento]:
        """Obtener alimentos por tipo"""
        return db.query(Alimento).filter(
            Alimento.tipo == tipo,
            Alimento.estado == EstadoAlimentoEnum.ACTIVO.value
        ).all()
    
    @staticmethod
    def _registrar_historial(
        db: Session,
        alimento_id: int,
        accion: str,
        usuario_id: int = None,
        datos_anteriores: str = None,
        motivo: str = None
    ):
        """Registrar acción en historial de alimentos"""
        historial = HistorialAlimento(
            alimento_id=alimento_id,
            accion=accion,
            usuario_accion=str(usuario_id) if usuario_id else None,
            datos_anteriores=datos_anteriores,
            motivo=motivo
        )
        
        db.add(historial)
        db.commit()
