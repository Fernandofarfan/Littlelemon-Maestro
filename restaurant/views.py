from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, viewsets
from .models import Menu, Reservation, Category
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib import messages

# Create your views here.
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
def home(request):
    return render(request, 'restaurant/home.html')

def contact(request):
    return render(request, 'restaurant/contact.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('signin')
        else:
            for field, error_messages in form.errors.items():
                for error in error_messages:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
        
    print(messages)
    return render(request, 'restaurant/register.html', {'form': form})

def signin(request):
    if(request.method == 'POST'):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_restaurant')
        else:
            messages.error(request, 'Invalid login details')
    else:
        form = AuthenticationForm()
    return render(request, 'restaurant/login.html', {'form': form})

def logoff(request):
    logout(request)
    return redirect('home_restaurant')

def menu(request, category_id=None):
    categories = Category.objects.all().filter(menu__isnull=False).distinct()
    if category_id:
        items = Menu.objects.filter(category__id=category_id)
    else:
        items = Menu.objects.all()
    
    return render(request, 'restaurant/menu.html', {'items': items, 'categories': categories})


    