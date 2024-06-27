from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import MenuViewSet, TableViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'tables', TableViewSet)
router.register(r'reservations', ReservationViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
]