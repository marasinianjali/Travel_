from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.tour_package.models import TourPackage
from rest_framework import generics
from .serializers import TourPackageSerializer, TourismCompanySerializer
from .permissions import IsAdminOrTourismCompany, IsUser, IsAdmin


class TourPackageListCreate(generics.ListCreateAPIView):
    # List and create view for TourPackage
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer

    # Only admin and tourism company can access this view
    permission_classes = [IsAdminOrTourismCompany]  # Adjust this as per your requirement
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['package_name', 'package_price', 'package_duration']
    search_fields = ['package_name', 'package_price', 'package_duration']
    ordering_fields = ['package_name', 'package_price', 'package_duration']
    ordering = ['package_name']  # Default ordering by package_name

# Retrieve, Update, Destroy view for only admin and tourism company 
class TourPackageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, and destroy view for TourPackage
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer
    permission_classes = [IsAdminOrTourismCompany]  # Only admin or tourism company can access this view
    lookup_field = 'package_id'  # Use package_id as the lookup field instead of pk


# Separate Tour Package update for admin only
class TourPackageAdmin(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, and destroy view for TourPackage by Admin only
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer
    permission_classes = [IsAdmin]  # Only admin can access this view
    lookup_field = 'package_id'  # Use package_id as the lookup field instead of pk

class TourPackageUserDetail(generics.RetrieveAPIView):
    # Retrieve, update, and destroy view for TourPackage
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer
    lookup_field = 'package_id'  # Use package_id as the lookup field instead of pk