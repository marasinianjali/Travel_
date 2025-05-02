from django.urls import path
from . import views

urlpatterns = [
    path('reviews_list/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    # path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]