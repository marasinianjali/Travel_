from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Guide
from .serializers import GuideSerializer
from .permissions import IsAdminOrManager, IsCustomer

# List and Create Guides
class GuideListCreateAPIView(generics.ListCreateAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [IsAdminOrManager]  # Manager or Admin can create; all can view
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tour_packages']
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'id']
    ordering = ['name']

# Retrieve, Update, Delete Guides (Admin or Manager)
class GuideRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [IsAdminOrManager]

# Separate Update and Delete Permissions (Only Admin can update or delete)
class GuideAdminUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [permissions.IsAdminUser]  # Only Admins

# Customer View (Only Viewing, No update or delete)
class GuideCustomerListAPIView(generics.ListAPIView):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
    permission_classes = [IsCustomer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'id']
    ordering = ['name']