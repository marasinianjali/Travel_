from django.urls import path
from . import views
from django.urls import path, include

app_name='guides'
urlpatterns = [
    path('guides/', views.guide_list, name='guide_list'),
    path('create/', views.guide_create, name='guide_create'),
    path('<int:pk>/', views.guide_edit_delete, name='guide_detail'),
    path('<int:pk>/edit/', views.guide_update, name='guide_update'),
    path('<int:pk>/delete/', views.guide_delete, name='guide_delete'),
    path('guide/<slug:slug>/', views.guide_view, name='guide_view'),
    
    path('api/', include('apps.Guides.api_urls')),

]


   