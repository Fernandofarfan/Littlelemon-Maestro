from django.test import TestCase
from .models import Menu, Reservation, Table, Category
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

# Create your tests here.

class MenuTestCase(TestCase):
    def setUp(self):
        # Crear categoría primero
        self.category = Category.objects.create(name="Entradas")
        
        # Crear items de menú
        self.pizza = Menu.objects.create(
            title="Pizza", 
            price=12.50, 
            description="Pizza de pepperoni", 
            category=self.category
        )
        self.pasta = Menu.objects.create(
            title="Pasta", 
            price=8.50, 
            description="Pasta de alfredo", 
            category=self.category
        )
        
    def test_menu_items(self):
        pizza = Menu.objects.get(title="Pizza")
        pasta = Menu.objects.get(title="Pasta")
        self.assertEqual(pizza.price, 12.50)
        self.assertEqual(pasta.price, 8.50)
        
    def test_menu_str(self):
        self.assertEqual(str(self.pizza), "Pizza Pizza de pepperoni")


class TableTestCase(TestCase):
    def setUp(self):
        self.table = Table.objects.create(name="Mesa 1", no_of_seats=4)
        
    def test_table_creation(self):
        self.assertEqual(self.table.name, "Mesa 1")
        self.assertEqual(self.table.no_of_seats, 4)
        self.assertTrue(self.table.available)
        
    def test_mark_unavailable(self):
        self.table.mark_unavailable()
        self.assertFalse(self.table.available)
        
    def test_mark_available(self):
        self.table.mark_unavailable()
        self.table.mark_available()
        self.assertTrue(self.table.available)


class ReservationTestCase(TestCase):
    def setUp(self):
        self.table = Table.objects.create(name="Mesa 1", no_of_seats=4)
        
    def test_reservation_creation(self):
        future_date = timezone.now() + timedelta(days=1)
        reservation = Reservation.objects.create(
            name="Juan Pérez",
            no_of_guest=2,
            booking_date=future_date.date(),
            booking_time=future_date.time(),
            table=self.table
        )
        self.assertEqual(reservation.name, "Juan Pérez")
        self.assertEqual(reservation.no_of_guest, 2)
        
    def test_reservation_past_date_validation(self):
        past_date = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            reservation = Reservation(
                name="Juan Pérez",
                no_of_guest=2,
                booking_date=past_date.date(),
                booking_time=past_date.time(),
                table=self.table
            )
            reservation.save()
            
    def test_reservation_exceeds_capacity(self):
        future_date = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            reservation = Reservation(
                name="Juan Pérez",
                no_of_guest=10,  # Excede capacidad de 4
                booking_date=future_date.date(),
                booking_time=future_date.time(),
                table=self.table
            )
            reservation.save()