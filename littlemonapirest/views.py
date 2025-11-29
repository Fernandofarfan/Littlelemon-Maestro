from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from restaurant.models import Menu, Category, Table, Reservation
from .serializers import MenuSerializer, CategorySerializer, TableSerializer, ReservationSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver categorías.
    Solo lectura para todos los usuarios.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver el menú.
    Solo lectura para todos los usuarios.
    Los administradores pueden crear/editar/eliminar desde el admin panel.
    """
    queryset = Menu.objects.select_related('category').all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title']
    ordering = ['category', 'title']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Endpoint personalizado para obtener items por categoría.
        GET /api/menu/by_category/?category=1
        """
        category_id = request.query_params.get('category')
        if category_id:
            items = self.queryset.filter(category_id=category_id)
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        return Response({"error": "Se requiere el parámetro 'category'"}, status=status.HTTP_400_BAD_REQUEST)


class TableViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para ver mesas.
    Solo lectura para usuarios autenticados.
    Los administradores pueden gestionar desde el admin panel.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['available', 'no_of_seats']
    ordering_fields = ['no_of_seats', 'name']
    ordering = ['no_of_seats']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """
        Endpoint para obtener solo mesas disponibles.
        GET /api/tables/available/
        """
        available_tables = self.queryset.filter(available=True)
        serializer = self.get_serializer(available_tables, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reservas.
    Los usuarios pueden crear, ver y cancelar sus propias reservas.
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna solo las reservas del usuario actual.
        Los administradores pueden ver todas.
        """
        user = self.request.user
        if user.is_staff:
            return Reservation.objects.select_related('table').all()
        
        # Filtrar por nombre del usuario
        user_name = user.get_full_name() or user.username
        return Reservation.objects.select_related('table').filter(name__icontains=user_name)
    
    def perform_create(self, serializer):
        """
        Al crear una reserva, usar el nombre del usuario si no se especifica.
        """
        name = serializer.validated_data.get('name')
        if not name or name == "No name":
            user = self.request.user
            name = user.get_full_name() or user.username
            serializer.save(name=name)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_reservations(self, request):
        """
        Endpoint para obtener las reservas del usuario actual.
        GET /api/reservations/my_reservations/
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def future(self, request):
        """
        Endpoint para obtener solo reservas futuras.
        GET /api/reservations/future/
        """
        from django.utils import timezone
        from datetime import datetime
        
        queryset = self.get_queryset()
        future_reservations = []
        
        for reservation in queryset:
            reservation_datetime = timezone.make_aware(
                datetime.combine(reservation.booking_date, reservation.booking_time)
            )
            if reservation_datetime >= timezone.now():
                future_reservations.append(reservation)
        
        serializer = self.get_serializer(future_reservations, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Cancelar una reserva (solo si es futura).
        """
        from django.utils import timezone
        from datetime import datetime
        
        instance = self.get_object()
        
        # Verificar que la reserva es futura
        reservation_datetime = timezone.make_aware(
            datetime.combine(instance.booking_date, instance.booking_time)
        )
        
        if reservation_datetime < timezone.now():
            return Response(
                {"error": "No puedes cancelar una reserva pasada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(
            {"message": "Reserva cancelada exitosamente"},
            status=status.HTTP_204_NO_CONTENT
        )
