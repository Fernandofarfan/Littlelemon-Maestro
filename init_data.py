"""
Script para inicializar datos de prueba en la base de datos.
Ejecutar: python init_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'littlemon.settings')
django.setup()

from restaurant.models import Category, Table, Menu
from django.contrib.auth.models import User

print("🚀 Iniciando carga de datos de prueba...")

# Crear categorías
print("\n📂 Creando categorías...")
categories_data = [
    "Entradas",
    "Platos Principales", 
    "Postres",
    "Bebidas",
    "Ensaladas"
]

categories = {}
for cat_name in categories_data:
    cat, created = Category.objects.get_or_create(name=cat_name)
    categories[cat_name] = cat
    if created:
        print(f"  ✅ Categoría creada: {cat_name}")
    else:
        print(f"  ℹ️  Categoría ya existe: {cat_name}")

# Crear mesas
print("\n🪑 Creando mesas...")
tables_data = [
    ("Mesa 1", 2),
    ("Mesa 2", 2),
    ("Mesa 3", 4),
    ("Mesa 4", 4),
    ("Mesa 5", 6),
    ("Mesa 6", 6),
    ("Mesa 7", 8),
    ("Mesa VIP", 10),
]

for name, seats in tables_data:
    table, created = Table.objects.get_or_create(
        name=name,
        defaults={'no_of_seats': seats, 'available': True}
    )
    if created:
        print(f"  ✅ Mesa creada: {name} ({seats} personas)")
    else:
        print(f"  ℹ️  Mesa ya existe: {name}")

# Crear items de menú (sin imágenes para prueba)
print("\n🍽️  Creando items de menú...")
menu_items = [
    # Entradas
    ("Bruschetta", 8.50, "Pan tostado con tomate fresco, albahaca y aceite de oliva", "Entradas"),
    ("Ensalada Caprese", 9.00, "Tomate, mozzarella fresca y albahaca", "Entradas"),
    ("Calamares Fritos", 12.00, "Anillos de calamar crujientes con salsa tártara", "Entradas"),
    
    # Platos Principales
    ("Pizza Margherita", 14.50, "Salsa de tomate, mozzarella y albahaca fresca", "Platos Principales"),
    ("Pasta Carbonara", 15.00, "Pasta con panceta, huevo y queso parmesano", "Platos Principales"),
    ("Risotto de Hongos", 16.50, "Arroz arborio con hongos variados", "Platos Principales"),
    ("Salmón a la Parrilla", 22.00, "Filete de salmón con vegetales asados", "Platos Principales"),
    ("Filete Mignon", 28.00, "Filete de res con papas y salsa de vino", "Platos Principales"),
    
    # Postres
    ("Tiramisú", 7.50, "Clásico postre italiano con café y mascarpone", "Postres"),
    ("Panna Cotta", 6.50, "Crema italiana con coulis de frutos rojos", "Postres"),
    ("Cheesecake", 7.00, "Tarta de queso con base de galleta", "Postres"),
    
    # Bebidas
    ("Limonada Natural", 4.00, "Limonada fresca hecha en casa", "Bebidas"),
    ("Agua Mineral", 3.00, "Agua con o sin gas", "Bebidas"),
    ("Vino Tinto Copa", 8.00, "Selección de vinos tintos", "Bebidas"),
    ("Café Espresso", 3.50, "Café italiano auténtico", "Bebidas"),
    
    # Ensaladas
    ("Ensalada César", 10.00, "Lechuga romana, crutones, parmesano y aderezo césar", "Ensaladas"),
    ("Ensalada Griega", 9.50, "Tomate, pepino, cebolla, aceitunas y queso feta", "Ensaladas"),
]

for title, price, description, cat_name in menu_items:
    # Solo crear si no existe (para evitar duplicados)
    if not Menu.objects.filter(title=title).exists():
        try:
            Menu.objects.create(
                title=title,
                price=price,
                description=description,
                category=categories[cat_name],
                image=''  # Sin imagen por ahora
            )
            print(f"  ✅ Item creado: {title} (${price})")
        except Exception as e:
            print(f"  ❌ Error creando {title}: {e}")
    else:
        print(f"  ℹ️  Item ya existe: {title}")

# Crear usuario de prueba (opcional)
print("\n👤 Verificando usuario de prueba...")
if not User.objects.filter(username='demo').exists():
    user = User.objects.create_user(
        username='demo',
        email='demo@littlelemon.com',
        password='demo123',
        first_name='Usuario',
        last_name='Demo'
    )
    print("  ✅ Usuario de prueba creado:")
    print("     Username: demo")
    print("     Password: demo123")
else:
    print("  ℹ️  Usuario 'demo' ya existe")

print("\n✨ ¡Datos de prueba cargados exitosamente!")
print("\n📝 Resumen:")
print(f"   - Categorías: {Category.objects.count()}")
print(f"   - Mesas: {Table.objects.count()}")
print(f"   - Items de menú: {Menu.objects.count()}")
print(f"   - Usuarios: {User.objects.count()}")
print("\n🎉 ¡Listo para usar!")
