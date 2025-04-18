

from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'user_name', 'package', 'status', 'booking_date')
    search_fields = ('user_name', 'user__username', 'package__name', 'promecode')
    list_filter = ('status', 'booking_date', 'package')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
    readonly_fields = ('booking_id',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'package', 'hotel', 'guide')