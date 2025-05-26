# apps/tourism_company_api/urls.py
from django.urls import path
from .  api_views import(
    TourismCompanyListCreate,
    TourismCompanyRetrieveUpdateDestroyAPIView,
    TourismCompanyAdmin,
    TourismCompanyUserDetail,
    # IsAdminOrTourismCompanyOrAPIKey,
)


urlpatterns = [
    path('tourism-company/', TourismCompanyListCreate.as_view(), name='tourism_company'),
    #path('tourism-company/', IsAdminOrTourismCompanyOrAPIKey.as_view(), name='tourism_company'),
    path('tourism-company/<int:company_id>/', TourismCompanyRetrieveUpdateDestroyAPIView.as_view(), name='tourism_company_detail'),
    path('admin/tourism-company/<int:company_id>/', TourismCompanyAdmin.as_view(), name='tourism_company_admin'),
    path('user/tourism-company/<int:company_id>/', TourismCompanyUserDetail.as_view(), name='tourism_company_user_detail'),
]