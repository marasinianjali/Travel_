from django.urls import path, include
from . import views

app_name = 'user_login'


urlpatterns = [
    path('login/', views.login_view, name='login'),
  
    path('dashboard/', views.dashboard_view, name='admin-dashboard'),
    path('admin_logout/', views.admin_logout_view, name='admin_logout'),

    path('user-signup/', views.signup_view, name='user-signup'),
    path('user-login/', views.user_login_view, name='user-login'),
    path('logout/', views.user_logout_view, name='user_logout'),  # Add this line
    path('user_dashboard/',views.user_dashboard_view, name='user_dashboard'),
    path('user-details/', views.user_details_view, name='user_details'),

    
    # Book a Tour: POST endpoint to book a tour package
   
    path('users/', views.user_list, name='user_list'),
    path('user/<int:user_id>/', views.view_user, name='view_user'), 
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path("add-to-wishlist/", views.add_to_wishlist, name="add_to_wishlist"),
    path("add-trip/", views.add_trip, name="add_trip"),
    path("update-profile/", views.update_profile, name="update_profile"),

   
    path('update-trip/<int:trip_id>/', views.update_trip, name='update_trip'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('update-wishlist/<int:wishlist_id>/', views.update_wishlist, name='update_wishlist'),
    path('delete-wishlist/<int:wishlist_id>/', views.delete_wishlist, name='delete_wishlist'),

    # APIs URLS
    path('api/', include('apps.user_login.api_urls')),
    
]
