from django.urls import path
from . import api_views

urlpatterns = [
    path('reviews_list/', api_views.ReviewListCreateView.as_view(), name='review-list-create'),
    # path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]