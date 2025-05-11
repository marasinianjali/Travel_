from django.urls import path
from . import api_views

urlpatterns = [
    path('tour-package/', api_views.TourPackageListCreate.as_view(), name='tour_package'),
    path('tour-package/<int:package_id>/', api_views.TourPackageDetail.as_view(), name='tour_package_detail'),

]