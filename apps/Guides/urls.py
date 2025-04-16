from django.urls import path
from . import views
app_name='guides'
urlpatterns = [
    path('', views.guide_list, name='guide_list'),
    path('create/', views.guide_create, name='guide_create'),
    path('<int:pk>/', views.guide_detail, name='guide_detail'),
    path('<int:pk>/edit/', views.guide_update, name='guide_update'),
    path('<int:pk>/delete/', views.guide_delete, name='guide_delete'),
    path('guide/<int:guide_id>/', views.guide_view, name='guide_view'),

]


   