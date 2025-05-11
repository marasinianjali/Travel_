from django.urls import path
from . import api_views

urlpatterns = [
    # User endpoints
    path('users/', api_views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:id>/', api_views.UserDetailView.as_view(), name='user-detail'),

    # Wishlist endpoints
    path('wishlists/', api_views.WishlistListCreateView.as_view(), name='wishlist-list-create'),
    path('wishlists/<int:pk>/',api_views.WishlistDetailView.as_view(), name='wishlist-detail'),

    # Trip endpoints
    path('trips/', api_views.TripListCreateView.as_view(), name='trip-list-create'),
    path('trips/<int:pk>/', api_views.TripDetailView.as_view(), name='trip-detail'),

    # Notification endpoints
    path('notifications/', api_views.NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', api_views.NotificationDetailView.as_view(), name='notification-detail'),

    # Booking endpoints
    path('bookings/', api_views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:booking_id>/', api_views.BookingDetailView.as_view(), name='booking-detail'),

    # Guide endpoints
    path('guides/', api_views.GuideListCreateView.as_view(), name='guide-list-create'),
    path('guides/<int:id>/', api_views.GuideDetailView.as_view(), name='guide-detail'),

    # Language endpoints
    path('languages/', api_views.LanguageListCreateView.as_view(), name='language-list-create'),
    path('languages/<int:pk>/', api_views.LanguageDetailView.as_view(), name='language-detail'),

    # LoginAdmin endpoints
    path('admins/', api_views.LoginAdminListCreateView.as_view(), name='loginadmin-list-create'),
    path('admins/<int:pk>/', api_views.LoginAdminDetailView.as_view(), name='loginadmin-detail'),
]
