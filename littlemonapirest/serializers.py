from rest_framework import serializers
from restaurant.models import Menu, Category, Table, Reservation
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Menu
        fields = ['id', 'title', 'price', 'description', 'image', 'category', 'category_id']
        read_only_fields = ['id']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'no_of_seats', 'available']
        read_only_fields = ['id']


class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    table_id = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        source='table',
        write_only=True
    )
    
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'no_of_guest', 'booking_date', 'booking_time', 'table', 'table_id']
        read_only_fields = ['id']
    
    def validate(self, data):
        """
        Validar que la reserva sea válida
        """
        from django.utils import timezone
        from datetime import datetime
        from django.core.exceptions import ValidationError as DjangoValidationError
        
        booking_date = data.get('booking_date')
        booking_time = data.get('booking_time')
        no_of_guest = data.get('no_of_guest')
        table = data.get('table')
        
        # Validar fecha y hora futura
        if booking_date and booking_time:
            reservation_datetime = timezone.make_aware(datetime.combine(booking_date, booking_time))
            if reservation_datetime < timezone.now():
                raise serializers.ValidationError("La fecha y hora de la reserva no pueden estar en el pasado")
        
        # Validar capacidad
        if table and no_of_guest:
            if no_of_guest > table.no_of_seats:
                raise serializers.ValidationError(
                    f"El número de invitados ({no_of_guest}) excede la capacidad de la mesa ({table.no_of_seats})"
                )
        
        # Validar disponibilidad
        if booking_date and booking_time and table:
            existing = Reservation.objects.filter(
                booking_date=booking_date,
                booking_time=booking_time,
                table=table
            )
            
            # Excluir la reserva actual si es una actualización
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise serializers.ValidationError("La mesa ya está reservada para esta fecha y hora")
        
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
