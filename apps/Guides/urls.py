from django.urls import path
from . import views

urlpatterns = [
    path('guides/', views.guide_list, name='guide_list'),
    path('guide/<int:guide_id>/', views.guide_view, name='guide_view'),
    path('guide/<int:pk>/', views.guide_detail, name='guide_detail'),
    path('guide/create/', views.guide_create, name='guide_create'),
    path('guide/edit/<int:pk>/', views.guide_update, name='guide_update'),
    path('guide/delete/<int:guide_id>/', views.guide_delete, name='guide_delete'),
]
