from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('companies/', views.tourism_company_list, name='tourism_company_list'),
    path('company_dashboard/', views.company_dashboard_view, name='company_dashboard'),
    path('company_signup/', views.company_signup, name='company_signup'),
    path('company_login/', views.company_login, name='company_login'),
    path('company_logout/', views.company_logout, name='company_logout'),
    path('company/create/', views.tourism_company_create, name='tourism_company_create'),
    path("bookings/", views.company_bookings, name="company_bookings"),
    path('company/update/<int:pk>/', views.tourism_company_update, name='tourism_company_update'),
    path('company/delete/<int:pk>/', views.tourism_company_delete, name='tourism_company_delete'),

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
