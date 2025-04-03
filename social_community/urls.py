from django.urls import path
from . import views

app_name = 'social_community'

urlpatterns = [
    path('followed/', views.followed_list, name='followed_list'),
    path('followers/', views.followers_list, name='followers_list'),
    path('community/', views.community_features, name='community_features'),
    path('profile/<int:user_id>/', views.public_profile, name='public_profile'),
]