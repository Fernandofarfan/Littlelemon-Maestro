from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, viewsets
from .models import Menu, Reservation, Category, Table
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ReservationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'restaurant/home.html')

def contact(request):
    return render(request, 'restaurant/contact.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada exitosamente. Ya puedes iniciar sesión.")
            return redirect('signin')
        else:
            for field, error_messages in form.errors.items():
                for error in error_messages:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
        
    return render(request, 'restaurant/register.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('home_restaurant')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    return render(request, 'restaurant/login.html', {'form': form})

def logoff(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('home_restaurant')

def menu(request, category_id=None):
    categories = Category.objects.all().filter(menu__isnull=False).distinct()
    if category_id:
        items = Menu.objects.filter(category__id=category_id)
    else:
        items = Menu.objects.all()
    
    return render(request, 'restaurant/menu.html', {'items': items, 'categories': categories})


@login_required(login_url='signin')
def book_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            # Si el usuario no especificó un nombre, usar el nombre de usuario
            if not reservation.name or reservation.name == "No name":
                reservation.name = request.user.get_full_name() or request.user.username
            reservation.save()
            messages.success(request, f'¡Reserva confirmada para {reservation.booking_date} a las {reservation.booking_time}!')
            return redirect('my_reservations')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        # Pre-llenar el nombre con el del usuario
        initial_data = {
            'name': request.user.get_full_name() or request.user.username
        }
        form = ReservationForm(initial=initial_data)
    
    available_tables = Table.objects.filter(available=True).order_by('no_of_seats')
    return render(request, 'restaurant/book.html', {
        'form': form,
        'available_tables': available_tables
    })


@login_required(login_url='signin')
def my_reservations(request):
    # Obtener todas las reservas del usuario (usando el nombre)
    user_name = request.user.get_full_name() or request.user.username
    reservations = Reservation.objects.filter(name__icontains=user_name).order_by('-booking_date', '-booking_time')
    
    # Separar en futuras y pasadas
    now = timezone.now()
    future_reservations = []
    past_reservations = []
    
    for reservation in reservations:
        reservation_datetime = timezone.make_aware(datetime.combine(reservation.booking_date, reservation.booking_time))
        if reservation_datetime >= now:
            future_reservations.append(reservation)
        else:
            past_reservations.append(reservation)
    
    return render(request, 'restaurant/my_reservations.html', {
        'future_reservations': future_reservations,
        'past_reservations': past_reservations
    })


@login_required(login_url='signin')
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Verificar que la reserva pertenece al usuario
    user_name = request.user.get_full_name() or request.user.username
    if user_name.lower() not in reservation.name.lower():
        messages.error(request, 'No tienes permiso para cancelar esta reserva')
        return redirect('my_reservations')
    
    # Verificar que la reserva es futura
    reservation_datetime = timezone.make_aware(datetime.combine(reservation.booking_date, reservation.booking_time))
    if reservation_datetime < timezone.now():
        messages.error(request, 'No puedes cancelar una reserva pasada')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        reservation_info = f"{reservation.booking_date} a las {reservation.booking_time}"
        reservation.delete()
        messages.success(request, f'Reserva del {reservation_info} cancelada exitosamente')
        return redirect('my_reservations')
    
    return render(request, 'restaurant/cancel_reservation.html', {'reservation': reservation})


@login_required(login_url='signin')
def check_availability(request):
    """Vista AJAX para verificar disponibilidad de mesas"""
    if request.method == 'GET':
        date_str = request.GET.get('date')
        time_str = request.GET.get('time')
        guests = request.GET.get('guests')
        
        if not all([date_str, time_str, guests]):
            return JsonResponse({'error': 'Faltan parámetros'}, status=400)
        
        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            booking_time = datetime.strptime(time_str, '%H:%M').time()
            no_of_guests = int(guests)
        except ValueError:
            return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
        
        # Buscar mesas disponibles con capacidad suficiente
        suitable_tables = Table.objects.filter(
            available=True,
            no_of_seats__gte=no_of_guests
        ).order_by('no_of_seats')
        
        # Filtrar las que no estén reservadas en esa fecha/hora
        available_tables = []
        for table in suitable_tables:
            is_reserved = Reservation.objects.filter(
                table=table,
                booking_date=booking_date,
                booking_time=booking_time
            ).exists()
            
            if not is_reserved:
                available_tables.append({
                    'id': table.id,
                    'name': table.name,
                    'capacity': table.no_of_seats
                })
        
        return JsonResponse({
            'available': len(available_tables) > 0,
            'tables': available_tables,
            'message': f'Hay {len(available_tables)} mesa(s) disponible(s)' if available_tables else 'No hay mesas disponibles para esta fecha y hora'
        })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)