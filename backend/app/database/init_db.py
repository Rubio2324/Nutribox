"""
Script de inicialización de base de datos
Crea roles, tipos de membresía y datos de prueba
"""
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine, Base
from app.models.models import (
    Rol, TipoMembresia, Usuario, Alimento,
    RolEnum, TipoMembresiaEnum, EstadoAlimentoEnum
)
from app.core.security import get_password_hash


def init_db():
    """Inicializar base de datos con datos iniciales"""
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Rol).first():
            print("La base de datos ya está inicializada.")
            return
        
        print("Inicializando base de datos...")
        
        # Crear roles
        roles = [
            Rol(
                nombre=RolEnum.ADMINISTRADOR.value,
                descripcion="Administrador del sistema con acceso completo"
            ),
            Rol(
                nombre=RolEnum.USUARIO_PRINCIPAL.value,
                descripcion="Usuario padre/madre que gestiona loncheras"
            ),
            Rol(
                nombre=RolEnum.USUARIO_SECUNDARIO.value,
                descripcion="Usuario hijo que consulta sus loncheras"
            )
        ]
        
        for rol in roles:
            db.add(rol)
        
        db.commit()
        print("✓ Roles creados")
        
        # Crear tipos de membresía
        membresias = [
            TipoMembresia(
                nombre=TipoMembresiaEnum.BASICO.value,
                descripcion="Plan básico - solo visualización de menús",
                max_direcciones=0,
                permite_personalizacion=False,
                permite_restricciones=False,
                permite_estadisticas_avanzadas=False,
                precio_mensual=0.0
            ),
            TipoMembresia(
                nombre=TipoMembresiaEnum.ESTANDAR.value,
                descripcion="Plan estándar - agregar/eliminar loncheras predeterminadas",
                max_direcciones=1,
                permite_personalizacion=False,
                permite_restricciones=True,
                permite_estadisticas_avanzadas=False,
                precio_mensual=15000.0
            ),
            TipoMembresia(
                nombre=TipoMembresiaEnum.PREMIUM.value,
                descripcion="Plan premium - personalización completa de loncheras",
                max_direcciones=3,
                permite_personalizacion=True,
                permite_restricciones=True,
                permite_estadisticas_avanzadas=True,
                precio_mensual=30000.0
            )
        ]
        
        for membresia in membresias:
            db.add(membresia)
        
        db.commit()
        print("✓ Tipos de membresía creados")
        
        # Obtener IDs de roles y membresías
        rol_admin = db.query(Rol).filter(Rol.nombre == RolEnum.ADMINISTRADOR.value).first()
        rol_principal = db.query(Rol).filter(Rol.nombre == RolEnum.USUARIO_PRINCIPAL.value).first()
        membresia_basica = db.query(TipoMembresia).filter(
            TipoMembresia.nombre == TipoMembresiaEnum.BASICO.value
        ).first()
        membresia_estandar = db.query(TipoMembresia).filter(
            TipoMembresia.nombre == TipoMembresiaEnum.ESTANDAR.value
        ).first()
        membresia_premium = db.query(TipoMembresia).filter(
            TipoMembresia.nombre == TipoMembresiaEnum.PREMIUM.value
        ).first()
        
        # Crear usuarios de prueba
        usuarios_prueba = [
            Usuario(
                email="admin@nutribox.com",
                password_hash=get_password_hash("admin123"),
                nombre="Administrador",
                apellido="Sistema",
                telefono="3001234567",
                rol_id=rol_admin.id,
                tipo_membresia_id=membresia_premium.id,
                activo=True
            ),
            Usuario(
                email="usuario@nutribox.com",
                password_hash=get_password_hash("usuario123"),
                nombre="María",
                apellido="González",
                telefono="3009876543",
                rol_id=rol_principal.id,
                tipo_membresia_id=membresia_estandar.id,
                activo=True
            ),
            Usuario(
                email="premium@nutribox.com",
                password_hash=get_password_hash("premium123"),
                nombre="Carlos",
                apellido="Rodríguez",
                telefono="3101234567",
                rol_id=rol_principal.id,
                tipo_membresia_id=membresia_premium.id,
                activo=True
            )
        ]
        
        for usuario in usuarios_prueba:
            db.add(usuario)
        
        db.commit()
        print("✓ Usuarios de prueba creados")
        print("  - admin@nutribox.com / admin123 (Administrador)")
        print("  - usuario@nutribox.com / usuario123 (Usuario Estándar)")
        print("  - premium@nutribox.com / premium123 (Usuario Premium)")
        
        # Crear alimentos de ejemplo
        alimentos_ejemplo = [
            # Frutas
            Alimento(
                nombre="Manzana",
                tipo="Fruta",
                descripcion="Manzana roja fresca",
                calorias=52,
                proteinas=0.3,
                carbohidratos=14,
                grasas=0.2,
                fibra=2.4,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Banana",
                tipo="Fruta",
                descripcion="Banana madura",
                calorias=89,
                proteinas=1.1,
                carbohidratos=23,
                grasas=0.3,
                fibra=2.6,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Naranja",
                tipo="Fruta",
                descripcion="Naranja fresca",
                calorias=47,
                proteinas=0.9,
                carbohidratos=12,
                grasas=0.1,
                fibra=2.4,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            # Proteínas
            Alimento(
                nombre="Sandwich de pollo",
                tipo="Proteína",
                descripcion="Sandwich integral con pechuga de pollo",
                calorias=250,
                proteinas=20,
                carbohidratos=30,
                grasas=8,
                fibra=3,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Huevo duro",
                tipo="Proteína",
                descripcion="Huevo cocido",
                calorias=78,
                proteinas=6,
                carbohidratos=0.6,
                grasas=5,
                fibra=0,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            # Lácteos
            Alimento(
                nombre="Yogurt natural",
                tipo="Lácteo",
                descripcion="Yogurt natural sin azúcar",
                calorias=59,
                proteinas=3.5,
                carbohidratos=4.7,
                grasas=3.3,
                fibra=0,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Queso fresco",
                tipo="Lácteo",
                descripcion="Porción de queso fresco",
                calorias=98,
                proteinas=7,
                carbohidratos=1.4,
                grasas=7,
                fibra=0,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            # Carbohidratos
            Alimento(
                nombre="Pan integral",
                tipo="Carbohidrato",
                descripcion="Rebanada de pan integral",
                calorias=69,
                proteinas=3.6,
                carbohidratos=12,
                grasas=1,
                fibra=2,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Galletas integrales",
                tipo="Carbohidrato",
                descripcion="Paquete de galletas integrales",
                calorias=130,
                proteinas=2,
                carbohidratos=20,
                grasas=5,
                fibra=2,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            # Verduras
            Alimento(
                nombre="Zanahoria baby",
                tipo="Verdura",
                descripcion="Zanahorias baby crudas",
                calorias=35,
                proteinas=0.6,
                carbohidratos=8,
                grasas=0.2,
                fibra=2.3,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Tomates cherry",
                tipo="Verdura",
                descripcion="Tomates cherry frescos",
                calorias=18,
                proteinas=0.9,
                carbohidratos=3.9,
                grasas=0.2,
                fibra=1.2,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            # Bebidas
            Alimento(
                nombre="Jugo natural",
                tipo="Bebida",
                descripcion="Jugo de fruta natural sin azúcar",
                calorias=45,
                proteinas=0.5,
                carbohidratos=11,
                grasas=0.1,
                fibra=0.5,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Agua",
                tipo="Bebida",
                descripcion="Botella de agua",
                calorias=0,
                proteinas=0,
                carbohidratos=0,
                grasas=0,
                fibra=0,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            # Snacks saludables
            Alimento(
                nombre="Frutos secos",
                tipo="Snack",
                descripcion="Mix de nueces y almendras",
                calorias=170,
                proteinas=6,
                carbohidratos=6,
                grasas=15,
                fibra=3,
                estado=EstadoAlimentoEnum.ACTIVO.value
            ),
            Alimento(
                nombre="Granola",
                tipo="Snack",
                descripcion="Porción de granola casera",
                calorias=150,
                proteinas=4,
                carbohidratos=20,
                grasas=6,
                fibra=3,
                estado=EstadoAlimentoEnum.ACTIVO.value
            )
        ]
        
        for alimento in alimentos_ejemplo:
            db.add(alimento)
        
        db.commit()
        print(f"✓ {len(alimentos_ejemplo)} alimentos de ejemplo creados")
        
        print("\n✅ Base de datos inicializada correctamente!")
        print("\n📋 Para comenzar:")
        print("   1. Inicia el servidor: uvicorn app.main:app --reload")
        print("   2. Accede a la documentación: http://localhost:8000/docs")
        print("   3. Usa las credenciales de prueba para autenticarte")
        
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
