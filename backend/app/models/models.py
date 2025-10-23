"""
Modelos de base de datos - NutriBox
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.database.connection import Base
import enum


class RolEnum(str, enum.Enum):
    """Enum para roles de usuario"""
    ADMINISTRADOR = "Administrador"
    USUARIO_PRINCIPAL = "Usuario Principal"
    USUARIO_SECUNDARIO = "Usuario Secundario"


class TipoMembresiaEnum(str, enum.Enum):
    """Enum para tipos de membresía"""
    BASICO = "Básico"
    ESTANDAR = "Estándar"
    PREMIUM = "Premium"


class EstadoAlimentoEnum(str, enum.Enum):
    """Enum para estado de alimentos"""
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"


class EstadoLoncheraEnum(str, enum.Enum):
    """Enum para estado de loncheras"""
    BORRADOR = "Borrador"
    ASIGNADA = "Asignada"
    PERSONALIZADA = "Personalizada"
    CONFIRMADA = "Confirmada"
    ARCHIVADA = "Archivada"
    ELIMINADA = "Eliminada"


# ==================== MODELOS ====================

class Rol(Base):
    """Modelo de Rol de Usuario"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")


class TipoMembresia(Base):
    """Modelo de Tipo de Membresía"""
    __tablename__ = "tipos_membresia"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    max_direcciones = Column(Integer, default=0)
    permite_personalizacion = Column(Boolean, default=False)
    permite_restricciones = Column(Boolean, default=False)
    permite_estadisticas_avanzadas = Column(Boolean, default=False)
    precio_mensual = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="tipo_membresia")


class Usuario(Base):
    """Modelo de Usuario"""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    ultimo_acceso = Column(DateTime(timezone=True), nullable=True)
    activo = Column(Boolean, default=True)
    
    # Claves foráneas
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    tipo_membresia_id = Column(Integer, ForeignKey("tipos_membresia.id"), nullable=False)
    
    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    tipo_membresia = relationship("TipoMembresia", back_populates="usuarios")
    hijos = relationship("Hijo", back_populates="padre", cascade="all, delete-orphan")
    direcciones = relationship("Direccion", back_populates="usuario", cascade="all, delete-orphan")


class Hijo(Base):
    """Modelo de Hijo (Usuario Secundario)"""
    __tablename__ = "hijos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    grado_escolar = Column(String(50), nullable=True)
    colegio = Column(String(150), nullable=True)
    observaciones = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Clave foránea
    padre_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relaciones
    padre = relationship("Usuario", back_populates="hijos")
    loncheras = relationship("Lonchera", back_populates="hijo", cascade="all, delete-orphan")
    restricciones = relationship("Restriccion", back_populates="hijo", cascade="all, delete-orphan")


class Alimento(Base):
    """Modelo de Alimento"""
    __tablename__ = "alimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)  # Fruta, Verdura, Proteína, Carbohidrato, Lácteo, etc.
    descripcion = Column(Text, nullable=True)
    
    # Información nutricional
    calorias = Column(Float, nullable=False)
    proteinas = Column(Float, nullable=False)
    carbohidratos = Column(Float, nullable=False)
    grasas = Column(Float, default=0.0)
    fibra = Column(Float, default=0.0)
    
    # Estado
    estado = Column(String(20), default=EstadoAlimentoEnum.ACTIVO.value)
    imagen_url = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    loncheras_alimentos = relationship("LoncheraAlimento", back_populates="alimento")
    historial = relationship("HistorialAlimento", back_populates="alimento")
    inventario = relationship("Inventario", back_populates="alimento", uselist=False)


class Lonchera(Base):
    """Modelo de Lonchera"""
    __tablename__ = "loncheras"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_asignacion = Column(Date, nullable=False)
    estado = Column(String(20), default=EstadoLoncheraEnum.BORRADOR.value)
    es_predeterminada = Column(Boolean, default=False)
    
    # Clave foránea
    hijo_id = Column(Integer, ForeignKey("hijos.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    hijo = relationship("Hijo", back_populates="loncheras")
    alimentos = relationship("LoncheraAlimento", back_populates="lonchera", cascade="all, delete-orphan")


class LoncheraAlimento(Base):
    """Tabla intermedia Lonchera-Alimento"""
    __tablename__ = "lonchera_alimento"
    
    id = Column(Integer, primary_key=True, index=True)
    lonchera_id = Column(Integer, ForeignKey("loncheras.id"), nullable=False)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False)
    cantidad = Column(Integer, default=1)
    notas = Column(Text, nullable=True)
    
    # Relaciones
    lonchera = relationship("Lonchera", back_populates="alimentos")
    alimento = relationship("Alimento", back_populates="loncheras_alimentos")


class Direccion(Base):
    """Modelo de Dirección"""
    __tablename__ = "direcciones"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)  # Casa, Trabajo, etc.
    direccion_linea1 = Column(String(200), nullable=False)
    direccion_linea2 = Column(String(200), nullable=True)
    barrio = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    codigo_postal = Column(String(20), nullable=True)
    referencia = Column(Text, nullable=True)
    es_principal = Column(Boolean, default=False)
    
    # Clave foránea
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="direcciones")


class Restriccion(Base):
    """Modelo de Restricción Alimentaria"""
    __tablename__ = "restricciones"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)  # Alergia, Intolerancia, Preferencia, etc.
    descripcion = Column(Text, nullable=False)
    severidad = Column(String(20), nullable=False)  # Alta, Media, Baja
    activa = Column(Boolean, default=True)
    
    # Clave foránea
    hijo_id = Column(Integer, ForeignKey("hijos.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    hijo = relationship("Hijo", back_populates="restricciones")
    excepciones = relationship("Excepcion", back_populates="restriccion", cascade="all, delete-orphan")


class Excepcion(Base):
    """Modelo de Excepción a Restricción"""
    __tablename__ = "excepciones"
    
    id = Column(Integer, primary_key=True, index=True)
    motivo = Column(Text, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    autorizado_por = Column(String(100), nullable=True)
    
    # Clave foránea
    restriccion_id = Column(Integer, ForeignKey("restricciones.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    restriccion = relationship("Restriccion", back_populates="excepciones")


class Inventario(Base):
    """Modelo de Inventario de Alimentos"""
    __tablename__ = "inventario"
    
    id = Column(Integer, primary_key=True, index=True)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False, unique=True)
    cantidad_disponible = Column(Integer, default=0)
    cantidad_minima = Column(Integer, default=0)
    unidad_medida = Column(String(20), default="unidad")
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    # Relaciones
    alimento = relationship("Alimento", back_populates="inventario")
    movimientos = relationship("InventarioMovimiento", back_populates="inventario")


class InventarioMovimiento(Base):
    """Modelo de Movimientos de Inventario"""
    __tablename__ = "inventario_movimientos"
    
    id = Column(Integer, primary_key=True, index=True)
    inventario_id = Column(Integer, ForeignKey("inventario.id"), nullable=False)
    tipo_movimiento = Column(String(20), nullable=False)  # Entrada, Salida, Ajuste
    cantidad = Column(Integer, nullable=False)
    motivo = Column(Text, nullable=True)
    usuario_registro = Column(String(100), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    inventario = relationship("Inventario", back_populates="movimientos")


class HistorialAlimento(Base):
    """Modelo de Historial de Alimentos (Auditoría)"""
    __tablename__ = "historial_alimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    alimento_id = Column(Integer, ForeignKey("alimentos.id"), nullable=False)
    accion = Column(String(50), nullable=False)  # Eliminado, Restaurado, Modificado
    usuario_accion = Column(String(100), nullable=True)
    datos_anteriores = Column(Text, nullable=True)  # JSON con estado anterior
    motivo = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    alimento = relationship("Alimento", back_populates="historial")


class Bitacora(Base):
    """Modelo de Bitácora de Sistema"""
    __tablename__ = "bitacora"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=True)
    accion = Column(String(100), nullable=False)
    entidad = Column(String(50), nullable=False)
    entidad_id = Column(Integer, nullable=True)
    detalles = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
