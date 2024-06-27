from django.contrib import admin
from .models import Menu, Reservation, Category, Table

# Register your models here.
admin.site.register(Menu)
admin.site.register(Reservation)
admin.site.register(Category)
admin.site.register(Table)