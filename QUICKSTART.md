# 🚀 Guía de Inicio Rápido - NutriBox

## Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Navegar al directorio del backend
```bash
cd nutribox/backend
```

### 2. Crear entorno virtual (recomendado)
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos
```bash
python -m app.database.init_db
```

Este comando creará:
- ✅ Tablas de la base de datos
- ✅ Roles (Administrador, Usuario Principal, Usuario Secundario)
- ✅ Tipos de membresía (Básico, Estándar, Premium)
- ✅ Usuarios de prueba
- ✅ 15 alimentos de ejemplo

### 5. Ejecutar el servidor
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Acceder a la API
- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc
- **API Base**: http://localhost:8000/

## 🔐 Usuarios de Prueba

### Administrador
- **Email**: admin@nutribox.com
- **Password**: admin123
- **Permisos**: Acceso completo al sistema

### Usuario Estándar
- **Email**: usuario@nutribox.com
- **Password**: usuario123
- **Plan**: Estándar (1 dirección, agregar/eliminar loncheras predeterminadas)

### Usuario Premium
- **Email**: premium@nutribox.com
- **Password**: premium123
- **Plan**: Premium (3 direcciones, personalización completa de loncheras)

## 📝 Primeros Pasos

### 1. Autenticarse
En la documentación (http://localhost:8000/docs):

1. Ir a la sección **Autenticación**
2. Usar el endpoint `POST /api/auth/login`
3. Enviar credenciales:
```json
{
  "email": "admin@nutribox.com",
  "password": "admin123"
}
```
4. Copiar el `access_token` de la respuesta
5. Hacer clic en el botón "Authorize" (🔒) en la parte superior
6. Pegar el token en el formato: `Bearer {token}`
7. Hacer clic en "Authorize"

### 2. Explorar Alimentos
- `GET /api/alimentos/` - Listar todos los alimentos
- `GET /api/alimentos/activos` - Listar solo alimentos activos
- `GET /api/alimentos/buscar?q=manzana` - Buscar alimentos

### 3. Crear una Lonchera (usuarios autenticados)
- Primero debes tener un hijo registrado
- Luego puedes crear loncheras con el endpoint `POST /api/loncheras/`

## 🧪 Ejecutar Pruebas

```bash
# Instalar dependencias de pruebas (ya incluidas en requirements.txt)
pip install pytest pytest-asyncio pytest-cov httpx

# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=app

# Ejecutar con output detallado
pytest -v
```

## 🛠️ Estructura del Proyecto

```
nutribox/backend/
├── app/
│   ├── core/           # Configuración y seguridad
│   ├── database/       # Conexión y modelos de BD
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   ├── services/       # Lógica de negocio
│   ├── routers/        # Endpoints de la API
│   ├── utils/          # Utilidades
│   └── main.py         # Aplicación principal
├── tests/              # Pruebas unitarias
├── requirements.txt    # Dependencias
└── .env                # Variables de entorno
```

## 📋 Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/token` - Login OAuth2
- `GET /api/auth/me` - Información del usuario actual
- `POST /api/auth/logout` - Cerrar sesión

### Alimentos
- `GET /api/alimentos/` - Listar alimentos
- `GET /api/alimentos/{id}` - Obtener alimento
- `POST /api/alimentos/` - Crear alimento (admin)
- `PUT /api/alimentos/{id}` - Actualizar alimento (admin)
- `DELETE /api/alimentos/{id}` - Eliminar alimento (admin)
- `POST /api/alimentos/{id}/restaurar` - Restaurar alimento (admin)

### Loncheras
- `GET /api/loncheras/` - Listar loncheras
- `GET /api/loncheras/{id}` - Obtener lonchera con detalles
- `POST /api/loncheras/` - Crear lonchera
- `PUT /api/loncheras/{id}` - Actualizar lonchera
- `DELETE /api/loncheras/{id}` - Eliminar lonchera
- `POST /api/loncheras/{id}/alimentos` - Agregar alimento (Premium)
- `DELETE /api/loncheras/{id}/alimentos/{alimento_id}` - Quitar alimento (Premium)
- `GET /api/loncheras/{id}/resumen` - Resumen nutricional
- `POST /api/loncheras/{id}/confirmar` - Confirmar lonchera

## 🐛 Solución de Problemas

### Error: "No module named 'app'"
```bash
# Asegúrate de estar en el directorio correcto
cd nutribox/backend
# Y ejecutar desde ahí
python -m app.database.init_db
```

### Error: "Could not open database"
```bash
# Verificar permisos de escritura en el directorio
chmod 755 .
# O especificar ruta completa en .env
DATABASE_URL=sqlite:////ruta/completa/nutribox.db
```

### Error: "Port already in use"
```bash
# Usar otro puerto
uvicorn app.main:app --reload --port 8001
```

## 📚 Próximos Pasos

1. **Implementar Frontend**: Crear interfaz web con HTML/CSS/JS
2. **Agregar más funcionalidades**:
   - Gestión de hijos
   - Restricciones alimentarias
   - Direcciones
   - Estadísticas y reportes
3. **Desplegar en Azure**: Configurar para producción
4. **Agregar pruebas**: Completar suite de pruebas

## 💡 Consejos

- Usa la documentación interactiva en `/docs` para probar todos los endpoints
- Los usuarios con plan Básico solo pueden ver menús
- Los usuarios Estándar pueden agregar/eliminar loncheras predeterminadas
- Los usuarios Premium pueden personalizar loncheras completamente
- El administrador tiene acceso completo a todas las funcionalidades

## 🆘 Soporte

Para más información, consulta:
- Documentación completa del proyecto
- README.md principal
- Diagramas de arquitectura en la carpeta `/docs`
