from django.urls import path
from . import views

# urlpatterns = [
#     path('bookings/', hotel_booking_list, name='hotel_booking_list'),
#     path('bookings/add/', add_hotel_booking, name='add_hotel_booking'),
#     path('bookings/edit/<int:hotel_id>/', edit_hotel_booking, name='edit_hotel_booking'),
#     path('bookings/delete/<int:hotel_id>/', delete_hotel_booking, name='delete_hotel_booking'),
# ]

urlpatterns = [
    # Dashboard URL
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

]