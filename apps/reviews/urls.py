from django.urls import path, include
from .views import review_list, add_review

app_name = 'reviews'

urlpatterns = [
    path('review_list/', review_list, name='review_list'),
    path('add/', add_review, name='add_review'),

    # APIs URLS
    path('api/', include('apps.reviews.api_urls')),
]
