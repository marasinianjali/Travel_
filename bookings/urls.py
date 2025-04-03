# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking_list, name='booking_list'),
    path('create/', views.create_booking, name='create_booking'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]
