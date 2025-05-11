from django.urls import path
from .api_views import (
     HotelBookingListCreateView, HotelBookingDetailView,HotelRevenueListCreateView,HotelRevenueDetailView
)

app_name = 'guides_api'

urlpatterns = [
    path('hotelbook/add/',  HotelBookingListCreateView.as_view(), name='guide-list-create'),
    path('hotelbooking/<int:pk>/', HotelBookingDetailView.as_view(), name='guide-detail'),
    path('hotel/revenue/<int:pk>/',HotelRevenueListCreateView.as_view(), name='guide-admin-detail'),
    path('hotel/revenuedetail/', HotelRevenueDetailView.as_view(), name='guide-customer-list'),
]