from django.shortcuts import render

from apps.tourism_company.models import TourismCompany
from rest_framework import generics
from .serializers import TourismCompanySerializer


class TourismCompanyListCreate(generics.ListCreateAPIView):
    # List and create view for TourismCompany
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer

class TourismCompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, and destroy view for TourismCompany 
    queryset = TourismCompany.objects.all()
    serializer_class = TourismCompanySerializer
    lookup_field = 'company_id'  # Use company_id as the lookup field instead of pk