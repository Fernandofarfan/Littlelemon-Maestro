from django.test import TestCase

# Create your tests here.
from .models import Menu

class MenuTestCase(TestCase):
    def setUp(self):
        Menu.objects.create(title="Pizza", price=12.50, inventory=10, description="Pizza de pepperoni", image="https://www.google.com", category="Entrees")
        Menu.objects.create(title="Pasta", price=8.50, inventory=10, description="Pasta de alfredo", image="https://www.google.com", category="Entrees")
        
    def test_menu_items(self):
        pizza = Menu.objects.get(title="Pizza")
        pasta = Menu.objects.get(title="Pasta")
        self.assertEqual(pizza.price, 12.50)
        self.assertEqual(pasta.price, 8.50)