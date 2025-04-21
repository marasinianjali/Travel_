from django.urls import path
from . import views



urlpatterns = [
    # Dashboard URL
    
    path('hotel_login/', views.hotel_login_view, name='hotel_login'),
    path('hotel_logout/', views.logout_view, name='hotel_logout'),
    path('hotel_dashboard/', views.hotel_dashboard, name="hotel_dashboard"),
    path('hotel_revenue_list/', views.hotel_revenue_list, name='hotel_revenue_list'),
    # Hotel Booking URLs
    
    path('hotel-bookings/', views.hotel_booking_list, name='hotel_booking_list'),
    path('hotel-bookings/add/', views.add_hotel_booking, name='add_hotel_booking'),  # Corrected import
    path('hotel-bookings/edit/<int:hotel_id>/', views.edit_hotel_booking, name='edit_hotel_booking'),
    path('hotel-bookings/delete/<int:hotel_id>/', views.delete_hotel_booking, name='delete_hotel_booking'),
    
    # Hotel Room URLs
    path('rooms/view/<int:room_id>/', views.view_hotel_room, name='view_hotel_room'),
    path('rooms/', views.hotel_rooms_list, name='hotel_rooms_list'),
    path('rooms/add/', views.add_hotel_room, name='add_hotel_room'),
    path('rooms/edit/<int:room_id>/', views.edit_hotel_room, name='edit_hotel_room'),
    path('rooms/delete/<int:room_id>/', views.delete_hotel_room, name='delete_hotel_room'),
    path('hotel-revenue/delete/<int:revenue_id>/', views.delete_hotel_revenue, name='delete_hotel_revenue'),  # Delete hotel revenue
    path('hotel-revenue/<int:revenue_id>/', views.edit_hotel_revenue, name='edit_hotel_revenue'),  # Edit specific hotel revenue
    path('hotel_revenue/<int:revenue_id>/', views.view_hotel_revenue, name='view_hotel_revenue'),  # View specific hotel revenue
    
    path('hotel/<int:hotel_id>/add_room_availability/', views.add_room_availability, name='add_room_availability'),
    path('availability/edit/<int:pk>/', views.edit_availability, name='edit_availability'),
    path('availability/delete/<int:pk>/', views.delete_availability, name='delete_availability'),
    
    path('room-availability-list/', views.room_availability_list, name='room_availability_list'),
   
    path('hotel/<int:hotel_id>/room_availability/', views.view_room_availability, name='view_room_availability'),
    path('reports/', views.hotel_report_list, name='hotel_report_list'),
    path('reports/add/', views.hotel_report_create, name='hotel_report_create'),
    path('reports/update/<int:pk>/', views.hotel_report_update, name='hotel_report_update'),
    path('reports/delete/<int:pk>/', views.hotel_report_delete, name='hotel_report_delete'),
    
]