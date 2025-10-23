# NUTRIBOX - Plataforma de Gestión de Loncheras Escolares

## 📋 Descripción
NutriBox es una plataforma web desarrollada en Python que permite gestionar loncheras escolares mediante planes de membresía diferenciados (Básico, Estándar y Premium).

## 🏗️ Arquitectura
- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Despliegue**: Azure App Service

## 📁 Estructura del Proyecto
```
nutribox/
├── backend/          # API REST con FastAPI
│   ├── app/
│   │   ├── models/      # Modelos de datos (ORM)
│   │   ├── schemas/     # Schemas Pydantic
│   │   ├── services/    # Lógica de negocio
│   │   ├── routers/     # Endpoints API
│   │   ├── database/    # Configuración DB
│   │   └── utils/       # Utilidades
│   ├── tests/           # Pruebas unitarias
│   └── requirements.txt
├── frontend/         # Interfaz web
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
├── docs/            # Documentación
└── tests/           # Pruebas de integración
```

## 🚀 Instalación

### Requisitos Previos
- Python 3.10+
- pip
- PostgreSQL (opcional para producción)

### Configuración Local

1. Clonar el repositorio
```bash
cd nutribox
```

2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. Instalar dependencias
```bash
pip install -r backend/requirements.txt
```

4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Inicializar base de datos
```bash
cd backend
python -m app.database.init_db
```

6. Ejecutar servidor de desarrollo
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Planes de Membresía

| Funcionalidad | Básico | Estándar | Premium |
|--------------|--------|----------|---------|
| Ver menús predeterminados | ✅ | ✅ | ✅ |
| Agregar/Eliminar loncheras | ❌ | ✅ | ✅ |
| Personalizar loncheras | ❌ | ❌ | ✅ |
| Restricciones alimentarias | ❌ | ✅ | ✅ |
| Direcciones de entrega | 0 | 1 | 3 |
| Estadísticas básicas | ❌ | ✅ | ✅ |
| Estadísticas avanzadas | ❌ | ❌ | ✅ |
| Historial de alimentos | ❌ | ❌ | ✅ |

## 🧪 Pruebas

```bash
# Pruebas unitarias
pytest backend/tests/ -v

# Cobertura de código
pytest --cov=app backend/tests/
```

## 📚 Documentación API
Una vez ejecutado el servidor, acceder a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 👥 Autores
- Leal, Julián Steven - 67001277
- Rubio Ramírez, Luis David - 67001331
- Vilardi González, Jesús Manuel - 67001298

## 🏛️ Institución
Universidad Católica de Colombia
Facultad de Ingeniería
Programa de Ingeniería de Sistemas y Computación

## 📄 Licencia
Proyecto académico - 2025
