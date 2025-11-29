from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Reservation, Table
from django.utils import timezone
from datetime import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("El email ya está registrado")
        return email


class ReservationForm(forms.ModelForm):
    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.now().date().isoformat()
        }),
        label='Fecha de reserva'
    )
    
    booking_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label='Hora de reserva'
    )
    
    no_of_guest = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de personas'
        }),
        label='Número de invitados'
    )
    
    table = forms.ModelChoiceField(
        queryset=Table.objects.filter(available=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mesa',
        empty_label='Seleccione una mesa'
    )
    
    class Meta:
        model = Reservation
        fields = ['name', 'no_of_guest', 'booking_date', 'booking_time', 'table']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            })
        }
        labels = {
            'name': 'Nombre'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        no_of_guest = cleaned_data.get('no_of_guest')
        table = cleaned_data.get('table')
        
        if booking_date and booking_time:
            # Validar que la fecha y hora no sean en el pasado
            reservation_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))
            if reservation_datetime < timezone.now():
                raise ValidationError("La fecha y hora de la reserva no pueden estar en el pasado")
            
            # Validar horario de operación (11:00 - 23:00)
            if booking_time.hour < 11 or booking_time.hour >= 23:
                raise ValidationError("El horario de reservas es de 11:00 a 23:00")
        
        if table and no_of_guest:
            # Validar capacidad de la mesa
            if no_of_guest > table.no_of_seats:
                raise ValidationError(f"La mesa seleccionada tiene capacidad para {table.no_of_seats} personas. Por favor seleccione una mesa más grande.")
            
            # Validar disponibilidad de la mesa
            if booking_date and booking_time:
                existing_reservation = Reservation.objects.filter(
                    table=table,
                    booking_date=booking_date,
                    booking_time=booking_time
                ).exists()
                
                if existing_reservation:
                    raise ValidationError("La mesa seleccionada ya está reservada para esta fecha y hora. Por favor seleccione otra mesa u horario.")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar mesas por capacidad
        self.fields['table'].queryset = Table.objects.filter(available=True).order_by('no_of_seats')
        # Personalizar la visualización de las mesas
        self.fields['table'].label_from_instance = lambda obj: f"{obj.name} - Capacidad: {obj.no_of_seats} personas"
