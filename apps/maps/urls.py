from django.urls import path
from .views import add_location, location_list, location_detail

urlpatterns = [
    path('addlocation/', add_location, name='add_location'),
    path('locationlist/', location_list, name='location_list'),
    path('<int:location_id>/', location_detail, name='location_detail'),
]
