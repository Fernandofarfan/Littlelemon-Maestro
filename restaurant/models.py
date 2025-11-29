from django.db import models
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="Uncategorized")
    
    def __str__(self):
        return self.name

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="No title")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(max_length=500, default="No description available")
    image = models.ImageField(upload_to='menu_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)      
    
    def __str__(self):
        return self.title + " " + self.description 


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="No name")
    no_of_seats = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    
    def mark_unavailable(self):
        self.available = False
        self.save()

    def mark_available(self):
        self.available = True
        self.save()
        
    def __str__(self):
        return self.name + " " + str(self.no_of_seats) + " seats"

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="No name")
    no_of_guest = models.IntegerField(default=0)
    booking_date = models.DateField(default=timezone.now) 
    booking_time = models.TimeField(default=timezone.now)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)
    
    def clean(self):
        # Validar que la fecha y hora no sean en el pasado
        reservation_date_time = timezone.make_aware(datetime.combine(self.booking_date, self.booking_time))
        if reservation_date_time < timezone.now():
            raise ValidationError("La fecha y hora de la reserva no pueden estar en el pasado")
        
        # Validar que el número de invitados no exceda la capacidad de la mesa
        if self.no_of_guest > self.table.no_of_seats:
            raise ValidationError(f"El número de invitados ({self.no_of_guest}) excede la capacidad de la mesa ({self.table.no_of_seats})")
        
        # Validar que la mesa no esté ya reservada para esa fecha y hora (excluyendo la reserva actual si es una actualización)
        existing_reservations = Reservation.objects.filter(
            booking_date=self.booking_date, 
            booking_time=self.booking_time, 
            table=self.table
        )
        if self.pk:
            existing_reservations = existing_reservations.exclude(pk=self.pk)
        
        if existing_reservations.exists():
            raise ValidationError("La mesa ya está reservada para esta fecha y hora")
    
    def save(self, *args, **kwargs):
        # Solo validar y marcar mesa como no disponible en nuevas reservas
        is_new = not self.pk
        
        if is_new:
            self.clean()
            
        super().save(*args, **kwargs)
        
        # Marcar mesa como no disponible solo para nuevas reservas
        if is_new:
            self.table.mark_unavailable()
        
    def delete(self, *args, **kwargs):
        self.table.mark_available()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} - {self.booking_date} {self.booking_time}"