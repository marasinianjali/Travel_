from django.contrib import admin
from .models import HotelBooking, HotelRoom, HotelRevenue, RoomAvailability,HotelReport

# Registering the models in the Django admin site
admin.site.register(HotelBooking)
admin.site.register(HotelRoom)
admin.site.register(HotelRevenue)
admin.site.register(RoomAvailability)
admin.site.register(HotelReport)
# Added RoomAvailability model
