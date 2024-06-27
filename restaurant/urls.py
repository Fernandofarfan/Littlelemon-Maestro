from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home_restaurant'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('logoff/', views.logoff, name='logoff'),
    path('menu/', views.menu, name='menu'),
    path('menu/<int:category_id>/', views.menu, name='menu_category'),    
]
