from django.shortcuts import render
from rest_framework import generics
from apps.reviews.models import Review
from apps.reviews_api.serializers import ReviewSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    