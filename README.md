# Little Lemon - Sistema de Reservas de Restaurante

![Little Lemon Logo](static/assets/logo2_littlelemon.png)

## 📋 Descripción

Little Lemon es un sistema completo de gestión de reservas para restaurantes desarrollado con Django 5.0.3 y Django REST Framework. Permite a los clientes reservar mesas en línea, gestionar sus reservas, y explorar el menú del restaurante.

## ✨ Características Principales

- 🔐 **Sistema de Autenticación**: Registro e inicio de sesión de usuarios
- 📅 **Reservas en Línea**: Sistema completo de reservas con validación de disponibilidad
- 🍽️ **Gestión de Menú**: Visualización de platos organizados por categorías
- 👤 **Panel de Usuario**: Los usuarios pueden ver y cancelar sus reservas
- 🛠️ **Panel de Administración**: Gestión completa de mesas, reservas, menú y categorías
- 🌐 **API REST**: Endpoints para integración con otras aplicaciones
- ✅ **Validaciones Inteligentes**: Prevención de reservas duplicadas y validación de capacidad

## 🚀 Tecnologías Utilizadas

- **Backend**: Django 5.0.3
- **API**: Django REST Framework 3.15.2
- **Base de Datos**: SQLite (desarrollo) / MySQL (producción)
- **Autenticación API**: Djoser 2.2.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Gestión de Imágenes**: Pillow 10.2.0

## 📦 Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)
- MySQL (opcional, para producción)

## 🔧 Instalación

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd Littlelemon-Maestro
```

### 2. Crear Entorno Virtual

```bash
python -m venv env
```

### 3. Activar el Entorno Virtual

**Windows (PowerShell):**
```bash
env\Scripts\activate
```

**Windows (CMD):**
```bash
env\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura tus variables:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edita el archivo `.env` con tus configuraciones:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Para desarrollo con SQLite (por defecto)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Para producción con MySQL (descomentar y configurar)
# DB_ENGINE=django.db.backends.mysql
# DB_NAME=littlelemon
# DB_USER=tu_usuario
# DB_PASSWORD=tu_contraseña
# DB_HOST=127.0.0.1
# DB_PORT=3306
```

### 6. Aplicar Migraciones

```bash
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu cuenta de administrador.

### 8. Cargar Datos Iniciales (Opcional)

Puedes crear categorías y mesas desde el panel de administración o usar el shell de Django:

```bash
python manage.py shell
```

```python
from restaurant.models import Category, Table

# Crear categorías
Category.objects.create(name="Entradas")
Category.objects.create(name="Platos Principales")
Category.objects.create(name="Postres")
Category.objects.create(name="Bebidas")

# Crear mesas
Table.objects.create(name="Mesa 1", no_of_seats=2, available=True)
Table.objects.create(name="Mesa 2", no_of_seats=4, available=True)
Table.objects.create(name="Mesa 3", no_of_seats=6, available=True)
Table.objects.create(name="Mesa 4", no_of_seats=8, available=True)
```

### 9. Iniciar el Servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/home/`

## 📱 Uso de la Aplicación

### Para Clientes

1. **Registro**: Crea una cuenta en `/register/`
2. **Iniciar Sesión**: Accede con tus credenciales en `/signin/`
3. **Explorar Menú**: Visita `/menu/` para ver los platos disponibles
4. **Reservar Mesa**: Ve a `/book/` para hacer una reserva
5. **Mis Reservas**: Gestiona tus reservas en `/my-reservations/`

### Para Administradores

1. **Panel de Administración**: Accede a `/admin/` con tu cuenta de superusuario
2. **Gestionar Menú**: Agrega, edita o elimina platos y categorías
3. **Gestionar Mesas**: Configura las mesas disponibles
4. **Ver Reservas**: Consulta todas las reservas del sistema
5. **Gestionar Usuarios**: Administra las cuentas de usuario

## 🔌 API REST

La aplicación incluye endpoints de API REST para integración:

### Autenticación

```bash
# Obtener token
POST /auth/token/login/
{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}

# Cerrar sesión
POST /auth/token/logout/
```

### Endpoints Disponibles

- `GET /api/menu/` - Listar menú
- `GET /api/categories/` - Listar categorías
- `POST /api/reservations/` - Crear reserva (requiere autenticación)
- `GET /api/reservations/` - Listar mis reservas (requiere autenticación)
- `DELETE /api/reservations/{id}/` - Cancelar reserva (requiere autenticación)

## 🧪 Ejecutar Tests

```bash
python manage.py test restaurant
```

## 📁 Estructura del Proyecto

```
Littlelemon-Maestro/
├── littlemon/              # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── restaurant/             # App principal
│   ├── models.py           # Modelos (Menu, Reservation, Table, Category)
│   ├── views.py            # Vistas
│   ├── forms.py            # Formularios
│   ├── admin.py            # Configuración del admin
│   ├── urls.py             # URLs de la app
│   └── tests.py            # Tests
├── templates/              # Templates HTML
│   ├── bases/
│   │   └── base.html       # Template base
│   └── restaurant/
│       ├── home.html
│       ├── menu.html
│       ├── book.html
│       ├── my_reservations.html
│       └── ...
├── static/                 # Archivos estáticos
│   ├── assets/             # Imágenes y logos
│   └── restaurant/
│       └── styles/
│           └── style.css
├── media/                  # Archivos subidos (imágenes de menú)
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🐛 Solución de Problemas

### Error: "No module named 'decouple'"

```bash
pip install python-decouple
```

### Error: "No module named 'PIL'"

```bash
pip install Pillow
```

### Error de conexión a MySQL

Asegúrate de:
1. Tener MySQL instalado y corriendo
2. Haber creado la base de datos: `CREATE DATABASE littlelemon;`
3. Configurar correctamente las credenciales en `.env`
4. Tener instalado `mysqlclient`: `pip install mysqlclient`

### Las imágenes del menú no se muestran

```bash
python manage.py collectstatic
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autor

Fernando Farfan

## 📞 Soporte

Para reportar bugs o solicitar features, por favor abre un issue en el repositorio.

---

**¡Disfruta de Little Lemon! 🍋**
