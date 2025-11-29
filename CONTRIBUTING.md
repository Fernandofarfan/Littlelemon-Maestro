# Contribuir a Little Lemon

¡Gracias por tu interés en contribuir a Little Lemon! 🎉

## 🤝 Cómo Contribuir

### 1. Fork el Proyecto

Haz un fork del repositorio en GitHub.

### 2. Crea una Rama

```bash
git checkout -b feature/nueva-funcionalidad
```

Convenciones de nombres de ramas:
- `feature/` - Nueva funcionalidad
- `fix/` - Corrección de bugs
- `docs/` - Documentación
- `refactor/` - Refactorización de código
- `test/` - Agregar o mejorar tests

### 3. Haz tus Cambios

Asegúrate de:
- Seguir el estilo de código del proyecto
- Agregar tests para nueva funcionalidad
- Actualizar la documentación si es necesario
- Mantener los commits atómicos y descriptivos

### 4. Ejecuta los Tests

```bash
python manage.py test
```

### 5. Commit tus Cambios

Usa mensajes de commit descriptivos:

```bash
git commit -m "feat: agregar filtro de búsqueda en menú"
git commit -m "fix: corregir validación de fecha en reservas"
git commit -m "docs: actualizar README con instrucciones de API"
```

Convenciones de commits:
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato (no afectan el código)
- `refactor:` - Refactorización de código
- `test:` - Agregar o modificar tests
- `chore:` - Tareas de mantenimiento

### 6. Push a tu Fork

```bash
git push origin feature/nueva-funcionalidad
```

### 7. Crea un Pull Request

Abre un Pull Request en GitHub con:
- Título descriptivo
- Descripción detallada de los cambios
- Referencias a issues relacionados (si aplica)
- Screenshots (si hay cambios visuales)

## 📋 Guías de Estilo

### Python

Seguimos [PEP 8](https://pep8.org/):
- Indentación de 4 espacios
- Líneas máximo 79 caracteres (flexible a 100 para código)
- Nombres de variables en `snake_case`
- Nombres de clases en `PascalCase`
- Constantes en `UPPER_CASE`

### Django

- Usar class-based views cuando sea apropiado
- Mantener views delgadas, lógica en models/services
- Usar Django ORM, evitar SQL raw cuando sea posible
- Agregar docstrings a funciones y clases

### JavaScript

- Usar `const` y `let`, evitar `var`
- Nombres de variables en `camelCase`
- Usar comillas simples para strings
- Agregar comentarios para lógica compleja

### CSS

- Usar variables CSS para colores y espaciado
- Nombres de clases descriptivos en `snake_case`
- Mobile-first approach
- Evitar `!important` cuando sea posible

## 🧪 Tests

### Escribir Tests

Todos los cambios deben incluir tests:

```python
from django.test import TestCase
from .models import Reservation

class ReservationTestCase(TestCase):
    def setUp(self):
        # Configuración inicial
        pass
    
    def test_crear_reserva_valida(self):
        # Test de funcionalidad
        pass
```

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app específica
python manage.py test restaurant

# Test específico
python manage.py test restaurant.tests.ReservationTestCase.test_crear_reserva_valida
```

## 📝 Documentación

### Docstrings

Usa docstrings para funciones y clases:

```python
def crear_reserva(usuario, mesa, fecha, hora):
    """
    Crea una nueva reserva para un usuario.
    
    Args:
        usuario (User): Usuario que hace la reserva
        mesa (Table): Mesa a reservar
        fecha (date): Fecha de la reserva
        hora (time): Hora de la reserva
    
    Returns:
        Reservation: Objeto de reserva creado
    
    Raises:
        ValidationError: Si la mesa no está disponible
    """
    pass
```

### Comentarios

- Explica el "por qué", no el "qué"
- Mantén comentarios actualizados
- Usa comentarios para TODOs: `# TODO: Implementar validación adicional`

## 🐛 Reportar Bugs

### Antes de Reportar

1. Verifica que el bug no esté ya reportado
2. Asegúrate de estar usando la última versión
3. Intenta reproducir el bug

### Cómo Reportar

Incluye:
- Descripción clara del bug
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots (si aplica)
- Versión de Python y Django
- Sistema operativo

Ejemplo:

```markdown
**Descripción**
La validación de fecha en reservas permite fechas pasadas.

**Pasos para Reproducir**
1. Ir a /book/
2. Seleccionar fecha de ayer
3. Intentar crear reserva

**Comportamiento Esperado**
Debe mostrar error de validación

**Comportamiento Actual**
Permite crear la reserva

**Entorno**
- Python 3.11
- Django 5.0.3
- Windows 11
```

## 💡 Sugerir Funcionalidades

### Antes de Sugerir

1. Verifica que no esté ya sugerida
2. Asegúrate de que encaje con el proyecto
3. Piensa en casos de uso

### Cómo Sugerir

Incluye:
- Descripción clara de la funcionalidad
- Problema que resuelve
- Propuesta de implementación (opcional)
- Ejemplos de uso

## ✅ Checklist de Pull Request

Antes de enviar tu PR, verifica:

- [ ] El código sigue las guías de estilo
- [ ] Los tests pasan (`python manage.py test`)
- [ ] Se agregaron tests para nueva funcionalidad
- [ ] La documentación está actualizada
- [ ] Los commits son descriptivos
- [ ] No hay conflictos con `main`
- [ ] Se probó manualmente la funcionalidad

## 🎯 Áreas de Contribución

### Fácil (Good First Issue)
- Mejorar documentación
- Corregir typos
- Agregar tests
- Mejorar mensajes de error

### Intermedio
- Agregar validaciones
- Mejorar UI/UX
- Optimizar queries
- Agregar filtros en API

### Avanzado
- Implementar nuevas funcionalidades
- Optimización de performance
- Seguridad
- Internacionalización

## 📞 Contacto

¿Preguntas? Puedes:
- Abrir un issue en GitHub
- Enviar email a: fernando@littlelemon.com
- Unirte a nuestro Discord (próximamente)

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer de la participación en nuestro proyecto una experiencia libre de acoso para todos.

### Nuestros Estándares

**Comportamiento esperado:**
- Ser respetuoso con diferentes puntos de vista
- Aceptar críticas constructivas
- Enfocarse en lo mejor para la comunidad
- Mostrar empatía hacia otros miembros

**Comportamiento inaceptable:**
- Uso de lenguaje o imágenes sexualizadas
- Comentarios insultantes o despectivos
- Acoso público o privado
- Publicar información privada de otros

### Aplicación

Instancias de comportamiento inaceptable pueden ser reportadas contactando al equipo del proyecto.

---

## 🙏 Agradecimientos

¡Gracias por contribuir a Little Lemon! Cada contribución, grande o pequeña, es valiosa.

**Contributors:**
- Fernando Farfan - Creador y mantenedor principal

---

**¡Feliz coding! 🚀**
