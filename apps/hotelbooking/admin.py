
from django.contrib import admin
from .models import Guide, Language, HotelBooking, HotelRoom, RoomAvailability, HotelRevenue, HotelReport

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_years', 'rating')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('languages',)

admin.site.register(Language)
admin.site.register(HotelBooking)
admin.site.register(HotelRoom)
admin.site.register(RoomAvailability)
admin.site.register(HotelRevenue)
admin.site.register(HotelReport)
