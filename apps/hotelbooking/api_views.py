from rest_framework import generics, permissions
from .models import  HotelBooking, HotelRevenue
from .serializers import (
     HotelBookingSerializer,
     HotelRevenueSerializer
)
class HotelBookingListCreateView(generics.ListCreateAPIView):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HotelBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer

class HotelRevenueListCreateView(generics.ListCreateAPIView):
    queryset = HotelRevenue.objects.all()
    serializer_class = HotelRevenueSerializer

class HotelRevenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelRevenue.objects.all()
    serializer_class = HotelRevenueSerializer
    
