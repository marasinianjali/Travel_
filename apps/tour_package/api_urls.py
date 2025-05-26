from django.urls import path
from . import api_views

urlpatterns = [
    path('tour-package/', api_views.TourPackageListCreate.as_view(), name='tour_package'),
    path('tour-package/<int:package_id>/', api_views.TourPackageRetrieveUpdateDestroyAPIView.as_view(), name='tour_package_detail'),
    path('admin/tour-package/<int:package_id>/', api_views.TourPackageAdmin.as_view(), name='tour_package_admin'),
    path('user/tour-package/<int:package_id>/', api_views.TourPackageUserDetail.as_view(), name='tour_package_detail'),


]