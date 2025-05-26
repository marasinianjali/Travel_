from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.tourism_company.models import TourismCompany
from rest_framework import generics
from .serializers import TourismCompanySerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions
from .permissions import IsAdminOrTourismCompany, IsUser, IsAdmin


# API keys 
# from rest_framework_api_key.permissions import HasAPIKey
# class TourismCompanyListCreate(generics.ListCreateAPIView):
#     # List and create view for TourismCompany 
#     queryset = TourismCompany.objects.all()
#     serializer_class = TourismCompanySerializer
#     # Only admin and tourism company can access this view
#     permission_classes = [HasAPIKey] 
    
from .permissions import IsAdminOrTourismCompanyOrAPIKey

class TourismCompanyListCreate(generics.ListCreateAPIView):
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer
    permission_classes = [IsAdminOrTourismCompanyOrAPIKey]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company_name', 'company_phone', 'company_address']
    search_fields = ['company_name', 'company_phone', 'company_address']
    ordering_fields = ['company_name', 'company_phone', 'company_address']
    ordering = ['company_name']









# class TourismCompanyListCreate(generics.ListCreateAPIView):
#     # List and create view for TourismCompany 
#     queryset = TourismCompany.objects.all()
#     serializer_class = TourismCompanySerializer
#     # Only admin and tourism company can access this view
#     permission_classes = [IsAdminOrTourismCompany] 
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
#     filterset_fields = ['company_name', 'company_phone', 'company_address']
#     search_fields = ['company_name', 'company_phone', 'company_address']
#     ordering_fields = ['company_name', 'company_phone', 'company_address']
#     ordering = ['company_name']  # Default ordering by company_name
# permission_classes = [HasAPIKey | IsAdminOrTourismCompany] 




# Retrieve, Update, Destroy view for TourismCompany by Admin or TourismCompany
class TourismCompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer
    permission_classes = [IsAdminOrTourismCompany]  # Only admin or tourism company can access this view
    lookup_field = 'company_id'  # Use company_id as the lookup field instead of pk

# Retrieve, Update, Destroy view for TourismCompany by Admin only
class TourismCompanyAdmin(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer
    permission_classes = [IsAdmin]  # Only admin can access this view
    lookup_field = 'company_id'  # Use company_id as the lookup field instead of pk


# Separate Tourism Company detail for user 
class TourismCompanyUserDetail(generics.RetrieveAPIView):
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer
    permission_classes = [IsUser]  # Only admin or tourism company can access this view
    lookup_field = 'company_id'  # Use company_id as the lookup field instead of pk