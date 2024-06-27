from rest_framework import serializers
from restaurant.models import Menu, Reservation, Table

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
        
class ReservationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Reservation
        fields = '__all__'
        
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'