# apps/tourism_company_api/urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path('tourism-company/', api_views.TourismCompanyListCreate.as_view(), name='tourism_company'),
    path('tourism-company/<int:company_id>/', api_views.TourismCompanyDetail.as_view(), name='tourism_company_detail'),
]