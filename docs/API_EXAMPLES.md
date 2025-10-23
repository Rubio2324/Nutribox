# 📚 Ejemplos de Uso - API NutriBox

## Autenticación

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@nutribox.com",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_info": {
    "id": 1,
    "email": "admin@nutribox.com",
    "nombre": "Administrador",
    "apellido": "Sistema",
    "rol_id": 1,
    "tipo_membresia_id": 3
  }
}
```

### Obtener información del usuario actual
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer {tu_token_aqui}"
```

## Gestión de Alimentos

### Listar todos los alimentos
```bash
curl -X GET "http://localhost:8000/api/alimentos/" \
  -H "Authorization: Bearer {token}"
```

### Listar solo alimentos activos
```bash
curl -X GET "http://localhost:8000/api/alimentos/activos" \
  -H "Authorization: Bearer {token}"
```

### Buscar alimentos
```bash
curl -X GET "http://localhost:8000/api/alimentos/buscar?q=manzana" \
  -H "Authorization: Bearer {token}"
```

### Obtener alimento específico
```bash
curl -X GET "http://localhost:8000/api/alimentos/1" \
  -H "Authorization: Bearer {token}"
```

### Crear nuevo alimento (solo administradores)
```bash
curl -X POST "http://localhost:8000/api/alimentos/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pera",
    "tipo": "Fruta",
    "descripcion": "Pera fresca y jugosa",
    "calorias": 57,
    "proteinas": 0.4,
    "carbohidratos": 15,
    "grasas": 0.1,
    "fibra": 3.1
  }'
```

### Actualizar alimento (solo administradores)
```bash
curl -X PUT "http://localhost:8000/api/alimentos/1" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "calorias": 55,
    "descripcion": "Manzana roja fresca y crujiente"
  }'
```

### Eliminar alimento (solo administradores)
```bash
curl -X DELETE "http://localhost:8000/api/alimentos/1" \
  -H "Authorization: Bearer {token}"
```

### Restaurar alimento eliminado (solo administradores)
```bash
curl -X POST "http://localhost:8000/api/alimentos/1/restaurar" \
  -H "Authorization: Bearer {token}"
```

## Gestión de Loncheras

### Listar loncheras del usuario
```bash
curl -X GET "http://localhost:8000/api/loncheras/" \
  -H "Authorization: Bearer {token}"
```

### Filtrar loncheras por hijo
```bash
curl -X GET "http://localhost:8000/api/loncheras/?hijo_id=1" \
  -H "Authorization: Bearer {token}"
```

### Obtener lonchera específica con detalles
```bash
curl -X GET "http://localhost:8000/api/loncheras/1" \
  -H "Authorization: Bearer {token}"
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Lonchera Lunes",
  "descripcion": "Lonchera balanceada",
  "fecha_asignacion": "2025-10-24",
  "estado": "Confirmada",
  "hijo_id": 1,
  "alimentos": [
    {
      "id": 1,
      "nombre": "Manzana",
      "tipo": "Fruta",
      "cantidad": 1,
      "calorias": 52,
      "proteinas": 0.3,
      "carbohidratos": 14
    },
    {
      "id": 4,
      "nombre": "Sandwich de pollo",
      "tipo": "Proteína",
      "cantidad": 1,
      "calorias": 250,
      "proteinas": 20,
      "carbohidratos": 30
    }
  ],
  "resumen_nutricional": {
    "total_calorias": 302,
    "total_proteinas": 20.3,
    "total_carbohidratos": 44,
    "total_grasas": 8.2,
    "total_fibra": 5.4,
    "num_alimentos": 2
  }
}
```

### Crear nueva lonchera
```bash
curl -X POST "http://localhost:8000/api/loncheras/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Lonchera Martes",
    "descripcion": "Lonchera con frutas",
    "fecha_asignacion": "2025-10-25",
    "hijo_id": 1,
    "alimentos": [
      {
        "alimento_id": 1,
        "cantidad": 1,
        "notas": "Manzana verde"
      },
      {
        "alimento_id": 2,
        "cantidad": 1
      }
    ]
  }'
```

### Agregar alimento a lonchera existente (Premium)
```bash
curl -X POST "http://localhost:8000/api/loncheras/1/alimentos" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "alimento_id": 6,
    "cantidad": 1,
    "notas": "Yogurt natural"
  }'
```

### Eliminar alimento de lonchera (Premium)
```bash
curl -X DELETE "http://localhost:8000/api/loncheras/1/alimentos/6" \
  -H "Authorization: Bearer {token}"
```

### Obtener resumen nutricional
```bash
curl -X GET "http://localhost:8000/api/loncheras/1/resumen" \
  -H "Authorization: Bearer {token}"
```

### Confirmar lonchera
```bash
curl -X POST "http://localhost:8000/api/loncheras/1/confirmar" \
  -H "Authorization: Bearer {token}"
```

### Actualizar lonchera
```bash
curl -X PUT "http://localhost:8000/api/loncheras/1" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Lonchera Lunes Actualizada",
    "descripcion": "Con más proteínas"
  }'
```

### Eliminar lonchera
```bash
curl -X DELETE "http://localhost:8000/api/loncheras/1" \
  -H "Authorization: Bearer {token}"
```

## Ejemplos con Python

### Usando requests
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/auth/login",
    json={
        "email": "admin@nutribox.com",
        "password": "admin123"
    }
)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Listar alimentos
alimentos = requests.get(
    "http://localhost:8000/api/alimentos/activos",
    headers=headers
).json()

print(f"Alimentos disponibles: {len(alimentos)}")

# Crear lonchera
nueva_lonchera = requests.post(
    "http://localhost:8000/api/loncheras/",
    headers=headers,
    json={
        "nombre": "Lonchera Saludable",
        "fecha_asignacion": "2025-10-24",
        "hijo_id": 1,
        "alimentos": [
            {"alimento_id": 1, "cantidad": 1},
            {"alimento_id": 4, "cantidad": 1}
        ]
    }
).json()

print(f"Lonchera creada: {nueva_lonchera['id']}")
```

## Ejemplos con JavaScript (Fetch API)

```javascript
// Login
async function login() {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'admin@nutribox.com',
      password: 'admin123'
    })
  });
  
  const data = await response.json();
  return data.access_token;
}

// Listar alimentos
async function getAlimentos(token) {
  const response = await fetch('http://localhost:8000/api/alimentos/activos', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return await response.json();
}

// Uso
(async () => {
  const token = await login();
  const alimentos = await getAlimentos(token);
  console.log('Alimentos:', alimentos);
})();
```

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos
- **401 Unauthorized**: No autenticado
- **403 Forbidden**: Sin permisos
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

## Notas Importantes

1. **Token de Autenticación**: Debe incluirse en todas las peticiones protegidas
2. **Permisos por Membresía**:
   - Básico: Solo visualización
   - Estándar: Agregar/eliminar loncheras predeterminadas
   - Premium: Personalización completa
3. **Formato de Fechas**: YYYY-MM-DD (ISO 8601)
4. **Paginación**: Usa `skip` y `limit` para controlar resultados

## Solución de Errores Comunes

### 401 Unauthorized
- Verifica que el token sea válido
- El token expira después de 30 minutos

### 403 Forbidden
- Verifica que tengas los permisos necesarios
- Algunas operaciones requieren rol de administrador o plan Premium

### 404 Not Found
- Verifica que el ID del recurso exista
- Comprueba que el recurso no haya sido eliminado
