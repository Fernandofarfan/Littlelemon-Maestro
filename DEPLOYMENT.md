# Guía de Despliegue - Little Lemon

Esta guía te ayudará a desplegar Little Lemon en producción.

## 🚀 Opciones de Despliegue

### Opción 1: Heroku (Recomendado para principiantes)

#### Prerrequisitos
- Cuenta en [Heroku](https://heroku.com)
- Heroku CLI instalado
- Git instalado

#### Pasos

1. **Preparar el proyecto**

Crear `Procfile`:
```
web: gunicorn littlemon.wsgi
```

Crear `runtime.txt`:
```
python-3.11.0
```

Actualizar `requirements.txt`:
```bash
pip freeze > requirements.txt
```

Agregar a requirements.txt:
```
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9
```

2. **Configurar settings.py para producción**

```python
import dj_database_url

# Agregar al final de settings.py
if not DEBUG:
    # WhiteNoise para archivos estáticos
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Base de datos PostgreSQL
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
    
    # Seguridad
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

3. **Crear app en Heroku**

```bash
heroku login
heroku create littlelemon-app
```

4. **Configurar variables de entorno**

```bash
heroku config:set SECRET_KEY="tu-secret-key-super-segura"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="littlelemon-app.herokuapp.com"
```

5. **Desplegar**

```bash
git add .
git commit -m "Preparar para despliegue en Heroku"
git push heroku main
```

6. **Migrar base de datos**

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

7. **Abrir aplicación**

```bash
heroku open
```

---

### Opción 2: Railway

#### Pasos

1. **Crear cuenta en [Railway](https://railway.app)**

2. **Conectar repositorio de GitHub**

3. **Configurar variables de entorno** en Railway:
```
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=tu-app.railway.app
DB_ENGINE=django.db.backends.postgresql
```

4. **Railway detectará automáticamente Django y desplegará**

5. **Ejecutar migraciones**:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

### Opción 3: DigitalOcean App Platform

#### Pasos

1. **Crear cuenta en [DigitalOcean](https://digitalocean.com)**

2. **Crear nueva App desde GitHub**

3. **Configurar**:
   - Tipo: Web Service
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn littlemon.wsgi`

4. **Agregar PostgreSQL Database**

5. **Configurar variables de entorno**

6. **Desplegar**

---

### Opción 4: VPS (Ubuntu) - Avanzado

#### Prerrequisitos
- VPS con Ubuntu 22.04
- Dominio configurado (opcional)

#### Pasos

1. **Conectar al servidor**
```bash
ssh root@tu-servidor-ip
```

2. **Actualizar sistema**
```bash
apt update && apt upgrade -y
```

3. **Instalar dependencias**
```bash
apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

4. **Crear usuario para la app**
```bash
adduser littlelemon
usermod -aG sudo littlelemon
su - littlelemon
```

5. **Clonar proyecto**
```bash
git clone https://github.com/tu-usuario/littlelemon-maestro.git
cd littlelemon-maestro
```

6. **Configurar entorno virtual**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

7. **Configurar PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE littlelemon;
CREATE USER littlelemonuser WITH PASSWORD 'password';
ALTER ROLE littlelemonuser SET client_encoding TO 'utf8';
ALTER ROLE littlelemonuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE littlelemonuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE littlelemon TO littlelemonuser;
\q
```

8. **Configurar .env**
```bash
nano .env
```

Contenido:
```
SECRET_KEY=tu-secret-key-super-segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=littlelemon
DB_USER=littlelemonuser
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

9. **Migrar y recolectar estáticos**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

10. **Configurar Gunicorn**

Crear `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=littlelemon
Group=www-data
WorkingDirectory=/home/littlelemon/littlelemon-maestro
ExecStart=/home/littlelemon/littlelemon-maestro/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/littlelemon/littlelemon-maestro/littlelemon.sock \
          littlemon.wsgi:application

[Install]
WantedBy=multi-user.target
```

Iniciar servicio:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

11. **Configurar Nginx**

Crear `/etc/nginx/sites-available/littlelemon`:
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/littlelemon/littlelemon-maestro;
    }
    
    location /media/ {
        root /home/littlelemon/littlelemon-maestro;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/littlelemon/littlelemon-maestro/littlelemon.sock;
    }
}
```

Activar sitio:
```bash
sudo ln -s /etc/nginx/sites-available/littlelemon /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

12. **Configurar SSL con Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

---

## 🔒 Checklist de Seguridad

Antes de desplegar a producción:

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` único y seguro
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Base de datos con credenciales seguras
- [ ] HTTPS habilitado (SSL/TLS)
- [ ] Archivos estáticos servidos correctamente
- [ ] Backups de base de datos configurados
- [ ] Variables de entorno en `.env` (no en git)
- [ ] `.gitignore` actualizado
- [ ] Logs configurados
- [ ] Monitoring configurado (opcional)

---

## 📊 Monitoreo

### Sentry (Errores)
```bash
pip install sentry-sdk
```

En settings.py:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="tu-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### New Relic (Performance)
```bash
pip install newrelic
```

---

## 🔄 Actualización en Producción

```bash
# Conectar al servidor
ssh usuario@servidor

# Ir al directorio del proyecto
cd littlelemon-maestro

# Activar entorno virtual
source env/bin/activate

# Obtener últimos cambios
git pull origin main

# Instalar nuevas dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic --noinput

# Reiniciar Gunicorn
sudo systemctl restart gunicorn

# Reiniciar Nginx
sudo systemctl restart nginx
```

---

## 📝 Notas Importantes

1. **Nunca** subas el archivo `.env` a Git
2. **Siempre** haz backup de la base de datos antes de actualizar
3. **Prueba** en un ambiente de staging primero
4. **Monitorea** los logs después del despliegue
5. **Documenta** cualquier configuración específica

---

## 🆘 Troubleshooting

### Error 500
- Verificar logs: `sudo journalctl -u gunicorn`
- Verificar `DEBUG = False` y `ALLOWED_HOSTS`

### Archivos estáticos no cargan
- Ejecutar `python manage.py collectstatic`
- Verificar configuración de Nginx

### Base de datos no conecta
- Verificar credenciales en `.env`
- Verificar que PostgreSQL esté corriendo

---

**¡Buena suerte con tu despliegue! 🚀**
