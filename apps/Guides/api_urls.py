from django.urls import path
from .api_views import (
    GuideListCreateAPIView,
    GuideRetrieveUpdateDestroyAPIView,
    GuideAdminUpdateDestroyAPIView,
    GuideCustomerListAPIView,
)

app_name = 'guides_api'

urlpatterns = [
    path('guides/', GuideListCreateAPIView.as_view(), name='guide-list-create'),
    path('guides/<int:pk>/', GuideRetrieveUpdateDestroyAPIView.as_view(), name='guide-detail'),
    path('admin/guides/<int:pk>/', GuideAdminUpdateDestroyAPIView.as_view(), name='guide-admin-detail'),
    path('customer/guides/', GuideCustomerListAPIView.as_view(), name='guide-customer-list'),
]