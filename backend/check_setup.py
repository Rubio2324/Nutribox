#!/usr/bin/env python3
"""
Script de verificación rápida del proyecto NutriBox
"""
import sys
import subprocess
import os

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.10+")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        import uvicorn
        print("✅ Dependencias principales instaladas")
        return True
    except ImportError as e:
        print(f"❌ Falta instalar dependencias: {e}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False

def check_database():
    """Verificar si la base de datos existe"""
    db_file = "nutribox.db"
    if os.path.exists(db_file):
        print(f"✅ Base de datos encontrada: {db_file}")
        return True
    else:
        print(f"⚠️  Base de datos no encontrada")
        print("   Ejecuta: python -m app.database.init_db")
        return False

def check_env_file():
    """Verificar archivo .env"""
    env_file = "../.env"
    if os.path.exists(env_file):
        print(f"✅ Archivo de configuración encontrado")
        return True
    else:
        print(f"⚠️  Archivo .env no encontrado")
        print("   Copia .env.example a .env")
        return False

def main():
    """Función principal"""
    print("=" * 50)
    print("🔍 Verificación del Proyecto NutriBox")
    print("=" * 50)
    print()
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
        check_database()
    ]
    
    print()
    print("=" * 50)
    
    if all(checks):
        print("✅ ¡Todo listo! Puedes iniciar el servidor:")
        print("   uvicorn app.main:app --reload")
    else:
        print("⚠️  Hay algunos problemas que resolver")
        print("   Revisa los mensajes anteriores")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
