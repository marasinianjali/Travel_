from django.shortcuts import render

from apps.tour_package.models import TourPackage
from rest_framework import generics
from .serializers import TourPackageSerializer, TourismCompanySerializer

class TourPackageListCreate(generics.ListCreateAPIView):
    # List and create view for TourPackage
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer

class TourPackageDetail(generics.RetrieveUpdateDestroyAPIView):
    # Retrieve, update, and destroy view for TourPackage
    queryset = TourPackage.objects.all()
    serializer_class = TourPackageSerializer
    lookup_field = 'package_id'  # Use package_id as the lookup field instead of pk