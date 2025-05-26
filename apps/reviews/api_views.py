from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from apps.reviews.models import Review
from . serializers import ReviewSerializer
from .permissions import IsAdminOrIsUser, IsUser, IsAdmin


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrIsUser]  # Only admin or user can access this view

class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrIsUser]  # Only admin or user can access this view
    lookup_field = 'review_id'  # Use review_id as the lookup field instead of pk


    