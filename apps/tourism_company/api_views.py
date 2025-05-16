from django.shortcuts import render

from apps.tourism_company.models import TourismCompany
from rest_framework import generics
from .serializers import TourismCompanySerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions


class PostUserWritePermission(BasePermission):
    """
    Custom permission to only allow owners of a post to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.owner == request.user



class TourismCompanyListCreate(generics.ListCreateAPIView):
    # List and create view for TourismCompany
    permission_classes = [DjangoModelPermissions]
    permission_classes = [IsAdminUser]  # Only admin users can access this view
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer

class TourismCompanyDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    # Retrieve, update, and destroy view for TourismCompany 
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer
    lookup_field = 'company_id'  # Use company_id as the lookup field instead of pk