from rest_framework import generics, permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS, IsAdminUser

from .models import HotelBooking, HotelRevenue
from .serializers import HotelBookingSerializer, HotelRevenueSerializer

# Custom permission to allow only owners or admins
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


# View to list and create hotel bookings
class HotelBookingListCreateView(generics.ListCreateAPIView):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return HotelBooking.objects.all()
        return HotelBooking.objects.filter(user=self.request.user)


# View to retrieve, update, or delete specific booking
class HotelBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


# Only admin users can access revenue info
class HotelRevenueListCreateView(generics.ListCreateAPIView):
    queryset = HotelRevenue.objects.all()
    serializer_class = HotelRevenueSerializer
    permission_classes = [IsAdminUser]


class HotelRevenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelRevenue.objects.all()
    serializer_class = HotelRevenueSerializer
    permission_classes = [IsAdminUser]