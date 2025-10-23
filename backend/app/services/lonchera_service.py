"""
Servicio de Lonchera - Lógica de negocio
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from app.models.models import (
    Lonchera, LoncheraAlimento, Alimento, Hijo, 
    EstadoLoncheraEnum, Usuario, TipoMembresia
)
from app.schemas.lonchera import (
    LoncheraCreate, LoncheraUpdate, 
    LoncheraAlimentoCreate, ResumenNutricional
)
from fastapi import HTTPException, status


class LoncheraService:
    """Servicio para gestión de loncheras"""
    
    @staticmethod
    def get_by_id(db: Session, lonchera_id: int) -> Optional[Lonchera]:
        """Obtener lonchera por ID"""
        return db.query(Lonchera).filter(Lonchera.id == lonchera_id).first()
    
    @staticmethod
    def get_all(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        hijo_id: Optional[int] = None,
        estado: Optional[str] = None
    ) -> List[Lonchera]:
        """Obtener lista de loncheras con filtros"""
        query = db.query(Lonchera)
        
        if hijo_id:
            query = query.filter(Lonchera.hijo_id == hijo_id)
        
        if estado:
            query = query.filter(Lonchera.estado == estado)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_por_fecha(
        db: Session, 
        hijo_id: int, 
        fecha: date
    ) -> Optional[Lonchera]:
        """Obtener lonchera de un hijo en una fecha específica"""
        return db.query(Lonchera).filter(
            Lonchera.hijo_id == hijo_id,
            Lonchera.fecha_asignacion == fecha
        ).first()
    
    @staticmethod
    def create(
        db: Session, 
        lonchera: LoncheraCreate, 
        usuario_id: int
    ) -> Lonchera:
        """Crear nueva lonchera"""
        # Verificar que el hijo existe y pertenece al usuario
        hijo = db.query(Hijo).filter(Hijo.id == lonchera.hijo_id).first()
        
        if not hijo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hijo no encontrado"
            )
        
        if hijo.padre_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para crear lonchera para este hijo"
            )
        
        # Verificar permisos según membresía
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        membresia = db.query(TipoMembresia).filter(
            TipoMembresia.id == usuario.tipo_membresia_id
        ).first()
        
        # Crear lonchera
        db_lonchera = Lonchera(
            nombre=lonchera.nombre,
            descripcion=lonchera.descripcion,
            fecha_asignacion=lonchera.fecha_asignacion,
            hijo_id=lonchera.hijo_id,
            estado=EstadoLoncheraEnum.BORRADOR.value
        )
        
        db.add(db_lonchera)
        db.commit()
        db.refresh(db_lonchera)
        
        # Agregar alimentos si se proporcionaron
        if lonchera.alimentos:
            for alimento_data in lonchera.alimentos:
                LoncheraService.agregar_alimento(
                    db, 
                    db_lonchera.id, 
                    alimento_data
                )
        
        return db_lonchera
    
    @staticmethod
    def update(
        db: Session, 
        lonchera_id: int, 
        lonchera_update: LoncheraUpdate,
        usuario_id: int
    ) -> Lonchera:
        """Actualizar lonchera"""
        db_lonchera = LoncheraService.get_by_id(db, lonchera_id)
        
        if not db_lonchera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lonchera no encontrada"
            )
        
        # Verificar permisos
        hijo = db.query(Hijo).filter(Hijo.id == db_lonchera.hijo_id).first()
        if hijo.padre_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para modificar esta lonchera"
            )
        
        # Actualizar campos
        update_data = lonchera_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_lonchera, field, value)
        
        db.commit()
        db.refresh(db_lonchera)
        
        return db_lonchera
    
    @staticmethod
    def delete(db: Session, lonchera_id: int, usuario_id: int) -> bool:
        """Eliminar lonchera"""
        db_lonchera = LoncheraService.get_by_id(db, lonchera_id)
        
        if not db_lonchera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lonchera no encontrada"
            )
        
        # Verificar permisos
        hijo = db.query(Hijo).filter(Hijo.id == db_lonchera.hijo_id).first()
        if hijo.padre_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para eliminar esta lonchera"
            )
        
        # Cambiar estado a eliminada (soft delete)
        db_lonchera.estado = EstadoLoncheraEnum.ELIMINADA.value
        db.commit()
        
        return True
    
    @staticmethod
    def agregar_alimento(
        db: Session, 
        lonchera_id: int, 
        alimento_data: LoncheraAlimentoCreate
    ) -> LoncheraAlimento:
        """Agregar alimento a lonchera"""
        # Verificar que el alimento existe
        alimento = db.query(Alimento).filter(
            Alimento.id == alimento_data.alimento_id
        ).first()
        
        if not alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado"
            )
        
        # Verificar si ya existe en la lonchera
        existe = db.query(LoncheraAlimento).filter(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == alimento_data.alimento_id
        ).first()
        
        if existe:
            # Actualizar cantidad
            existe.cantidad += alimento_data.cantidad
            db.commit()
            db.refresh(existe)
            return existe
        
        # Crear nuevo
        db_lonchera_alimento = LoncheraAlimento(
            lonchera_id=lonchera_id,
            alimento_id=alimento_data.alimento_id,
            cantidad=alimento_data.cantidad,
            notas=alimento_data.notas
        )
        
        db.add(db_lonchera_alimento)
        db.commit()
        db.refresh(db_lonchera_alimento)
        
        return db_lonchera_alimento
    
    @staticmethod
    def eliminar_alimento(
        db: Session, 
        lonchera_id: int, 
        alimento_id: int
    ) -> bool:
        """Eliminar alimento de lonchera"""
        db_lonchera_alimento = db.query(LoncheraAlimento).filter(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == alimento_id
        ).first()
        
        if not db_lonchera_alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado en la lonchera"
            )
        
        db.delete(db_lonchera_alimento)
        db.commit()
        
        return True
    
    @staticmethod
    def calcular_resumen_nutricional(
        db: Session, 
        lonchera_id: int
    ) -> ResumenNutricional:
        """Calcular resumen nutricional de una lonchera"""
        lonchera_alimentos = db.query(LoncheraAlimento).filter(
            LoncheraAlimento.lonchera_id == lonchera_id
        ).all()
        
        resumen = ResumenNutricional()
        
        for la in lonchera_alimentos:
            alimento = db.query(Alimento).filter(
                Alimento.id == la.alimento_id
            ).first()
            
            if alimento:
                resumen.total_calorias += alimento.calorias * la.cantidad
                resumen.total_proteinas += alimento.proteinas * la.cantidad
                resumen.total_carbohidratos += alimento.carbohidratos * la.cantidad
                resumen.total_grasas += alimento.grasas * la.cantidad
                resumen.total_fibra += alimento.fibra * la.cantidad
                resumen.num_alimentos += la.cantidad
        
        return resumen
    
    @staticmethod
    def confirmar(db: Session, lonchera_id: int, usuario_id: int) -> Lonchera:
        """Confirmar lonchera"""
        db_lonchera = LoncheraService.get_by_id(db, lonchera_id)
        
        if not db_lonchera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lonchera no encontrada"
            )
        
        # Verificar permisos
        hijo = db.query(Hijo).filter(Hijo.id == db_lonchera.hijo_id).first()
        if hijo.padre_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para confirmar esta lonchera"
            )
        
        db_lonchera.estado = EstadoLoncheraEnum.CONFIRMADA.value
        db.commit()
        db.refresh(db_lonchera)
        
        return db_lonchera
    
    @staticmethod
    def archivar(db: Session, lonchera_id: int) -> Lonchera:
        """Archivar lonchera (automático cuando pasa la fecha)"""
        db_lonchera = LoncheraService.get_by_id(db, lonchera_id)
        
        if not db_lonchera:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lonchera no encontrada"
            )
        
        db_lonchera.estado = EstadoLoncheraEnum.ARCHIVADA.value
        db.commit()
        db.refresh(db_lonchera)
        
        return db_lonchera
