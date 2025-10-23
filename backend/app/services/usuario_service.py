"""
Servicio de Usuario - Lógica de negocio
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from datetime import datetime
from backend.app.models.models import Usuario, Rol
from backend.app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from backend.app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status


class UsuarioService:
    """Servicio para gestión de usuarios"""
    
    @staticmethod
    def get_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def get_all(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        activo: Optional[bool] = None
    ) -> List[Usuario]:
        """Obtener lista de usuarios con paginación"""
        query = db.query(Usuario)
        
        if activo is not None:
            query = query.filter(Usuario.activo == activo)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, usuario: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        # Verificar si el email ya existe
        if UsuarioService.get_by_email(db, usuario.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Hash de la contraseña
        hashed_password = get_password_hash(usuario.password)
        
        # Crear usuario
        db_usuario = Usuario(
            email=usuario.email,
            password_hash=hashed_password,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            telefono=usuario.telefono,
            rol_id=usuario.rol_id,
            tipo_membresia_id=usuario.tipo_membresia_id
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def update(
        db: Session, 
        usuario_id: int, 
        usuario_update: UsuarioUpdate
    ) -> Usuario:
        """Actualizar usuario"""
        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Actualizar campos
        update_data = usuario_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_usuario, field, value)
        
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def change_password(
        db: Session, 
        usuario_id: int, 
        current_password: str, 
        new_password: str
    ) -> bool:
        """Cambiar contraseña de usuario"""
        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(current_password, db_usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Actualizar contraseña
        db_usuario.password_hash = get_password_hash(new_password)
        db.commit()
        
        return True
    
    @staticmethod
    def deactivate(db: Session, usuario_id: int) -> Usuario:
        """Desactivar usuario"""
        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        db_usuario.activo = False
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def activate(db: Session, usuario_id: int) -> Usuario:
        """Activar usuario"""
        db_usuario = UsuarioService.get_by_id(db, usuario_id)
        
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        db_usuario.activo = True
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        usuario = UsuarioService.get_by_email(db, email)
        
        if not usuario:
            return None
        
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario desactivado"
            )
        
        if not verify_password(password, usuario.password_hash):
            return None
        
        # Actualizar último acceso
        usuario.ultimo_acceso = datetime.utcnow()
        db.commit()
        
        return usuario
    
    @staticmethod
    def search(
        db: Session, 
        query: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Usuario]:
        """Buscar usuarios por nombre, apellido o email"""
        return db.query(Usuario).filter(
            or_(
                Usuario.nombre.ilike(f"%{query}%"),
                Usuario.apellido.ilike(f"%{query}%"),
                Usuario.email.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()
