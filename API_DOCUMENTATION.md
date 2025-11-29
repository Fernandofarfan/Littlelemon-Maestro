# API REST - Little Lemon

Documentación completa de la API REST de Little Lemon.

## 🔐 Autenticación

La API utiliza autenticación por token. Debes obtener un token antes de hacer requests a endpoints protegidos.

### Obtener Token

```bash
POST /auth/token/login/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```

**Respuesta exitosa:**
```json
{
    "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Usar el Token

Incluye el token en el header `Authorization` de tus requests:

```bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Cerrar Sesión

```bash
POST /auth/token/logout/
Authorization: Token {tu_token}
```

---

## 📋 Endpoints Disponibles

### Base URL
```
http://localhost:8000/api/
```

---

## 🍽️ Menú

### Listar Items del Menú

```bash
GET /api/menu/
```

**Parámetros opcionales:**
- `category`: Filtrar por ID de categoría
- `search`: Buscar en título y descripción
- `ordering`: Ordenar por `price`, `title`, `-price`, `-title`
- `page`: Número de página (paginación de 10 items)

**Ejemplo:**
```bash
curl -H "Authorization: Token {token}" \
  "http://localhost:8000/api/menu/?category=1&ordering=price"
```

**Respuesta:**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/menu/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Pizza Margherita",
            "price": "12.50",
            "description": "Pizza clásica con tomate y mozzarella",
            "image": "/media/menu_images/pizza.jpg",
            "category": {
                "id": 1,
                "name": "Platos Principales"
            }
        }
    ]
}
```

### Obtener Item Específico

```bash
GET /api/menu/{id}/
```

### Items por Categoría (Endpoint Personalizado)

```bash
GET /api/menu/by_category/?category={category_id}
```

---

## 📂 Categorías

### Listar Categorías

```bash
GET /api/categories/
```

**Respuesta:**
```json
[
    {
        "id": 1,
        "name": "Entradas"
    },
    {
        "id": 2,
        "name": "Platos Principales"
    }
]
```

### Obtener Categoría Específica

```bash
GET /api/categories/{id}/
```

---

## 🪑 Mesas

**Requiere autenticación**

### Listar Mesas

```bash
GET /api/tables/
Authorization: Token {tu_token}
```

**Parámetros opcionales:**
- `available`: Filtrar por disponibilidad (`true`/`false`)
- `no_of_seats`: Filtrar por número de asientos
- `ordering`: Ordenar por `no_of_seats`, `name`

**Respuesta:**
```json
[
    {
        "id": 1,
        "name": "Mesa 1",
        "no_of_seats": 4,
        "available": true
    }
]
```

### Mesas Disponibles (Endpoint Personalizado)

```bash
GET /api/tables/available/
Authorization: Token {tu_token}
```

---

## 📅 Reservas

**Requiere autenticación**

### Crear Reserva

```bash
POST /api/reservations/
Authorization: Token {tu_token}
Content-Type: application/json

{
    "name": "Juan Pérez",
    "no_of_guest": 4,
    "booking_date": "2025-12-01",
    "booking_time": "19:00:00",
    "table_id": 1
}
```

**Validaciones:**
- La fecha y hora deben ser futuras
- El número de invitados no puede exceder la capacidad de la mesa
- La mesa no debe estar reservada para esa fecha/hora

**Respuesta exitosa (201 Created):**
```json
{
    "id": 15,
    "name": "Juan Pérez",
    "no_of_guest": 4,
    "booking_date": "2025-12-01",
    "booking_time": "19:00:00",
    "table": {
        "id": 1,
        "name": "Mesa 1",
        "no_of_seats": 4,
        "available": true
    }
}
```

**Respuesta de error (400 Bad Request):**
```json
{
    "non_field_errors": [
        "La mesa ya está reservada para esta fecha y hora"
    ]
}
```

### Listar Mis Reservas

```bash
GET /api/reservations/
Authorization: Token {tu_token}
```

Retorna solo las reservas del usuario autenticado.

### Mis Reservas (Endpoint Personalizado)

```bash
GET /api/reservations/my_reservations/
Authorization: Token {tu_token}
```

### Reservas Futuras

```bash
GET /api/reservations/future/
Authorization: Token {tu_token}
```

Retorna solo las reservas futuras del usuario.

### Obtener Reserva Específica

```bash
GET /api/reservations/{id}/
Authorization: Token {tu_token}
```

### Actualizar Reserva

```bash
PUT /api/reservations/{id}/
Authorization: Token {tu_token}
Content-Type: application/json

{
    "name": "Juan Pérez",
    "no_of_guest": 6,
    "booking_date": "2025-12-01",
    "booking_time": "20:00:00",
    "table_id": 2
}
```

### Cancelar Reserva

```bash
DELETE /api/reservations/{id}/
Authorization: Token {tu_token}
```

**Validación:** Solo se pueden cancelar reservas futuras.

**Respuesta exitosa (204 No Content):**
```json
{
    "message": "Reserva cancelada exitosamente"
}
```

---

## 🔍 Filtros y Búsqueda

### Búsqueda en Menú

```bash
GET /api/menu/?search=pizza
```

Busca en los campos `title` y `description`.

### Ordenamiento

```bash
GET /api/menu/?ordering=price          # Ascendente
GET /api/menu/?ordering=-price         # Descendente
GET /api/menu/?ordering=title,-price   # Múltiples campos
```

### Paginación

```bash
GET /api/menu/?page=2
```

Cada página contiene 10 items por defecto.

---

## 📊 Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Request exitoso |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Recurso eliminado exitosamente |
| 400 | Bad Request - Datos inválidos |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - Sin permisos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## 💻 Ejemplos de Uso

### Python (requests)

```python
import requests

# Obtener token
response = requests.post('http://localhost:8000/auth/token/login/', json={
    'username': 'usuario',
    'password': 'contraseña'
})
token = response.json()['auth_token']

# Headers con autenticación
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Listar menú
menu = requests.get('http://localhost:8000/api/menu/', headers=headers)
print(menu.json())

# Crear reserva
reserva = requests.post('http://localhost:8000/api/reservations/', 
    headers=headers,
    json={
        'name': 'Juan Pérez',
        'no_of_guest': 4,
        'booking_date': '2025-12-01',
        'booking_time': '19:00:00',
        'table_id': 1
    }
)
print(reserva.json())
```

### JavaScript (fetch)

```javascript
// Obtener token
const loginResponse = await fetch('http://localhost:8000/auth/token/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        username: 'usuario',
        password: 'contraseña'
    })
});
const { auth_token } = await loginResponse.json();

// Listar menú
const menuResponse = await fetch('http://localhost:8000/api/menu/', {
    headers: {
        'Authorization': `Token ${auth_token}`
    }
});
const menu = await menuResponse.json();
console.log(menu);

// Crear reserva
const reservaResponse = await fetch('http://localhost:8000/api/reservations/', {
    method: 'POST',
    headers: {
        'Authorization': `Token ${auth_token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Juan Pérez',
        no_of_guest: 4,
        booking_date: '2025-12-01',
        booking_time: '19:00:00',
        table_id: 1
    })
});
const reserva = await reservaResponse.json();
console.log(reserva);
```

---

## 🛡️ Permisos

| Endpoint | Permiso Requerido |
|----------|-------------------|
| `/api/menu/` | Autenticado (lectura) |
| `/api/categories/` | Autenticado (lectura) |
| `/api/tables/` | Autenticado (lectura) |
| `/api/reservations/` (GET) | Autenticado (propias reservas) |
| `/api/reservations/` (POST) | Autenticado |
| `/api/reservations/{id}/` (PUT/DELETE) | Autenticado (propias reservas) |

**Nota:** Los administradores pueden ver y gestionar todas las reservas.

---

## 🔧 Configuración

Para habilitar la API en tu instalación:

1. Asegúrate de que `littlemonapirest` esté en `INSTALLED_APPS`
2. Las URLs de la API están en `/api/`
3. La autenticación está en `/auth/`

---

## 📝 Notas

- Todos los timestamps están en UTC
- Las fechas deben estar en formato ISO 8601 (`YYYY-MM-DD`)
- Las horas deben estar en formato 24h (`HH:MM:SS`)
- Los precios son decimales con 2 decimales
- Las imágenes se sirven desde `/media/`

---

**Versión de la API**: 1.0  
**Última actualización**: 28 de Noviembre, 2025
