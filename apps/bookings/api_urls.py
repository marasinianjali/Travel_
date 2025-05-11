from django.urls import path
from . import api_views

urlpatterns = [
    path('booking-list/', api_views.BookingListCreate.as_view(), name='tour_package'),
    path('booking-list/<int:booking_id>/', api_views.BookingDetail.as_view(), name='tour_package_detail'),
]