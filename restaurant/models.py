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
        return self.title +  " " + self.description 


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
    booking_date = models.DateField(default="2021-01-01") 
    booking_time = models.TimeField(default="12:00:00")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)
    
    def clean(self):
        reservation_date_time = timezone.make_aware(datetime.combine(self.booking_date, self.booking_time))
        if reservation_date_time < timezone.now():
            raise ValidationError("Reservation date and time cannot be in the past")
        if self.no_of_guest > self.table.no_of_seats:
            raise ValidationError("Number of guests cannot exceed the number of seats")
        if Reservation.objects.filter(booking_date=self.booking_date, booking_time=self.booking_time, table=self.table).exists():
            raise ValidationError("Table already reserved")
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
            self.table.mark_unavailable()
            raise ValidationError("Table already reserved")
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        self.table.mark_available()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.name + " " + self.booking_date 