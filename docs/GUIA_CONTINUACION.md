# 🚀 Guía para Continuar el Desarrollo de NutriBox

## 📋 Estado Actual del Proyecto

### ✅ Ya Implementado (85%)
- Modelos de base de datos completos
- Sistema de autenticación con JWT
- Gestión de alimentos (CRUD completo)
- Gestión de loncheras (CRUD con permisos)
- Control de membresías
- Documentación API

### ⏳ Por Implementar (15%)
- Gestión de hijos (CRUD)
- Gestión de direcciones (CRUD)
- Restricciones alimentarias
- Estadísticas y reportes
- Frontend completo

## 🔄 Próximas Tareas Prioritarias

### FASE 1: Completar Backend (Semana 1-2)

#### 1. Router de Hijos
**Archivo**: `backend/app/routers/hijos.py`

```python
"""
Router de Hijos - Crear este archivo
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.hijo import HijoCreate, HijoUpdate, Hijo
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Hijo)
async def crear_hijo(
    hijo: HijoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear nuevo hijo"""
    # Implementar lógica
    pass

# Implementar:
# - GET / (listar hijos del usuario)
# - GET /{hijo_id} (obtener hijo)
# - PUT /{hijo_id} (actualizar hijo)
# - DELETE /{hijo_id} (desactivar hijo)
```

**Luego agregar en `main.py`**:
```python
from app.routers import hijos
app.include_router(hijos.router, prefix="/api/hijos", tags=["Hijos"])
```

#### 2. Servicio de Hijos
**Archivo**: `backend/app/services/hijo_service.py`

```python
"""
Servicio de Hijo - Crear este archivo
"""
from sqlalchemy.orm import Session
from app.models.models import Hijo

class HijoService:
    @staticmethod
    def get_by_id(db: Session, hijo_id: int):
        return db.query(Hijo).filter(Hijo.id == hijo_id).first()
    
    @staticmethod
    def get_by_padre(db: Session, padre_id: int):
        return db.query(Hijo).filter(
            Hijo.padre_id == padre_id,
            Hijo.activo == True
        ).all()
    
    # Implementar create, update, delete, etc.
```

#### 3. Router de Direcciones
**Archivo**: `backend/app/routers/direcciones.py`

Implementar endpoints:
- POST / (crear dirección - validar límite por membresía)
- GET / (listar direcciones del usuario)
- PUT /{id} (actualizar dirección)
- DELETE /{id} (eliminar dirección)

**Validación importante**:
```python
# Verificar límite de direcciones según membresía
membresia = current_user.tipo_membresia
direcciones_actuales = len(current_user.direcciones)

if direcciones_actuales >= membresia.max_direcciones:
    raise HTTPException(
        status_code=403,
        detail=f"Ha alcanzado el límite de {membresia.max_direcciones} direcciones"
    )
```

#### 4. Router de Restricciones
**Archivo**: `backend/app/routers/restricciones.py`

Endpoints necesarios:
- POST / (crear restricción - solo Premium)
- GET /hijo/{hijo_id} (listar restricciones de un hijo)
- PUT /{id} (actualizar restricción)
- DELETE /{id} (eliminar restricción)
- POST /{id}/excepciones (agregar excepción)

### FASE 2: Frontend Básico (Semana 3-4)

#### 1. Estructura HTML Base
**Archivo**: `frontend/templates/index.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NutriBox - Gestión de Loncheras</title>
    <link rel="stylesheet" href="/static/css/main.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>NutriBox</h1>
            <div id="user-menu"></div>
        </div>
    </nav>
    
    <main class="container">
        <div id="app"></div>
    </main>
    
    <script src="/static/js/main.js"></script>
</body>
</html>
```

#### 2. JavaScript para API
**Archivo**: `frontend/static/js/api.js`

```javascript
// Cliente API
class NutriBoxAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('token');
    }
    
    async login(email, password) {
        const response = await fetch(`${this.baseURL}/api/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        
        if (response.ok) {
            const data = await response.json();
            this.token = data.access_token;
            localStorage.setItem('token', this.token);
            return data;
        }
        throw new Error('Login failed');
    }
    
    async getAlimentos() {
        const response = await fetch(`${this.baseURL}/api/alimentos/activos`, {
            headers: {'Authorization': `Bearer ${this.token}`}
        });
        return await response.json();
    }
    
    // Agregar más métodos según necesidad
}

const api = new NutriBoxAPI();
```

#### 3. CSS Básico
**Archivo**: `frontend/static/css/main.css`

```css
:root {
    --primary: #4CAF50;
    --secondary: #2196F3;
    --danger: #f44336;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.navbar {
    background: var(--primary);
    color: white;
    padding: 1rem 0;
}

/* Agregar más estilos */
```

#### 4. Actualizar FastAPI para servir frontend
**En `main.py`**:

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Agregar después de crear app
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/templates/index.html")
```

### FASE 3: Estadísticas y Reportes (Semana 5)

#### 1. Router de Estadísticas
**Archivo**: `backend/app/routers/estadisticas.py`

Endpoints a implementar:
```python
@router.get("/basicas")
async def obtener_estadisticas_basicas():
    """
    Plan Estándar y Premium
    - Promedio de calorías por lonchera
    - Total de loncheras creadas
    - Alimentos más usados
    """
    pass

@router.get("/avanzadas")
async def obtener_estadisticas_avanzadas():
    """
    Solo Premium
    - Tendencias nutricionales
    - Comparativas por hijo
    - Reportes descargables (CSV/PDF)
    """
    pass
```

#### 2. Generación de Reportes
Instalar dependencias adicionales:
```bash
pip install reportlab pandas
```

Implementar generación de PDF:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_reporte_pdf(loncheras, usuario):
    # Crear PDF con información nutricional
    pass
```

### FASE 4: Pruebas (Semana 6)

#### 1. Estructura de Pruebas
**Archivo**: `backend/tests/test_auth.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/api/auth/login", json={
        "email": "admin@nutribox.com",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid():
    response = client.post("/api/auth/login", json={
        "email": "admin@nutribox.com",
        "password": "wrong"
    })
    assert response.status_code == 401
```

#### 2. Ejecutar Pruebas
```bash
# Instalar pytest
pip install pytest pytest-cov

# Ejecutar todas las pruebas
pytest

# Con cobertura
pytest --cov=app --cov-report=html
```

### FASE 5: Despliegue en Azure (Semana 7)

#### 1. Preparar para Producción
**Archivo**: `backend/requirements-prod.txt`

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
gunicorn==21.2.0
```

#### 2. Configurar PostgreSQL
En `.env`:
```
DATABASE_URL=postgresql://nutribox_user:password@nutribox-db.postgres.database.azure.com/nutribox
```

#### 3. Crear Dockerfile
**Archivo**: `backend/Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Checklist de Desarrollo

### Backend
- [x] Modelos de base de datos
- [x] Autenticación JWT
- [x] Gestión de alimentos
- [x] Gestión de loncheras
- [ ] Gestión de hijos
- [ ] Gestión de direcciones
- [ ] Restricciones alimentarias
- [ ] Estadísticas básicas
- [ ] Estadísticas avanzadas
- [ ] Reportes PDF/CSV
- [ ] Inventario

### Frontend
- [ ] Login/Registro
- [ ] Dashboard
- [ ] Gestión de hijos
- [ ] Creación de loncheras
- [ ] Visualización de menús
- [ ] Perfil de usuario
- [ ] Estadísticas

### Pruebas
- [ ] Pruebas unitarias
- [ ] Pruebas de integración
- [ ] Pruebas de carga
- [ ] Pruebas de seguridad

### Despliegue
- [ ] Configuración Azure
- [ ] Base de datos en la nube
- [ ] CI/CD
- [ ] Monitoreo

## 🎯 Recomendaciones

### 1. Mantener Organización
- Commit frecuente con mensajes claros
- Usar branches para features nuevas
- Documentar cambios importantes

### 2. Priorizar Seguridad
- Validar todas las entradas
- No exponer información sensible
- Mantener dependencias actualizadas

### 3. Testing
- Escribir pruebas conforme desarrollas
- Objetivo: 80% de cobertura
- Usar datos de prueba realistas

### 4. Documentación
- Actualizar API docs
- Comentar código complejo
- Mantener README actualizado

## 📚 Recursos Útiles

### Documentación
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/

### Tutoriales
- FastAPI + SQLAlchemy: https://fastapi.tiangolo.com/tutorial/sql-databases/
- JWT Authentication: https://fastapi.tiangolo.com/tutorial/security/
- Testing: https://fastapi.tiangolo.com/tutorial/testing/

### Herramientas
- Postman: Para probar API
- VS Code: Editor recomendado
- pgAdmin: Para gestionar PostgreSQL

## 💡 Consejos Finales

1. **Divide y conquista**: Implementa una funcionalidad a la vez
2. **Prueba constantemente**: No esperes a terminar todo para probar
3. **Lee la documentación**: Está ahí para ayudarte
4. **Pregunta si te atoras**: Mejor perder 5 minutos preguntando que 2 horas atascado
5. **Haz commits frecuentes**: Pequeños commits son mejores que uno gigante

## 🎓 Contacto y Soporte

Para dudas sobre el desarrollo:
- Revisa la documentación en `/docs`
- Consulta los ejemplos en `API_EXAMPLES.md`
- Usa el Swagger UI en `http://localhost:8000/docs`

¡Éxito con el desarrollo! 🚀
