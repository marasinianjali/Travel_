# apps/tourism_company_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('tourism-company/', views.TourismCompanyListCreate.as_view(), name='tourism_company'),
    path('tourism-company/<int:company_id>/', views.TourismCompanyDetail.as_view(), name='tourism_company_detail'),
]