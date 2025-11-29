from django.contrib import admin
from .models import Menu, Reservation, Category, Table

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'description_preview')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    ordering = ('category', 'title')
    list_per_page = 20
    
    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Descripción'


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'no_of_seats', 'available', 'reservation_count')
    list_filter = ('available', 'no_of_seats')
    search_fields = ('name',)
    ordering = ('no_of_seats', 'name')
    actions = ['mark_as_available', 'mark_as_unavailable']
    
    def reservation_count(self, obj):
        return obj.reservation_set.count()
    reservation_count.short_description = 'Reservas Totales'
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} mesa(s) marcada(s) como disponible(s).')
    mark_as_available.short_description = 'Marcar como disponible'
    
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} mesa(s) marcada(s) como no disponible(s).')
    mark_as_unavailable.short_description = 'Marcar como no disponible'


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    fields = ('name', 'booking_date', 'booking_time', 'no_of_guest')
    readonly_fields = ('name', 'booking_date', 'booking_time', 'no_of_guest')
    can_delete = False


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'table', 'booking_date', 'booking_time', 'no_of_guest', 'is_future')
    list_filter = ('booking_date', 'table', 'no_of_guest')
    search_fields = ('name', 'table__name')
    ordering = ('-booking_date', '-booking_time')
    date_hierarchy = 'booking_date'
    list_per_page = 25
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('name', 'no_of_guest')
        }),
        ('Detalles de la Reserva', {
            'fields': ('table', 'booking_date', 'booking_time')
        }),
    )
    
    def is_future(self, obj):
        from django.utils import timezone
        from datetime import datetime
        reservation_datetime = timezone.make_aware(datetime.combine(obj.booking_date, obj.booking_time))
        is_future = reservation_datetime >= timezone.now()
        return '✓' if is_future else '✗'
    is_future.short_description = 'Futura'
    is_future.boolean = True
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('table')