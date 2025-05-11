from apps.bookings.models import Booking
from rest_framework import generics
from .serializers import BookingSerializer

class BookingListCreate(generics.ListCreateAPIView):
    # List and create view for Booking
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, and destroy view for Booking
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'booking_id'  # Use booking_id as the lookup field instead of pk

