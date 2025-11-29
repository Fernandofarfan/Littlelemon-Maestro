from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, CategoryViewSet, TableViewSet, ReservationViewSet

# Crear router y registrar viewsets
router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]
