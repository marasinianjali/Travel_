from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('packages/', views.tour_package_list, name='tour_package_list'),
    path('packages/add', views.add_tour_package, name='add_tour_package'),
   

    path("book/<int:package_id>/", views.book_tour, name="book_tour"),
   

    path('packages/review/<int:package_id>', views.review_package, name='review_package'),
    path('packages/edit/<int:package_id>/', views.edit_tour_package, name='edit_tour_package'),
    path('packages/delete/<int:package_id>/', views.delete_tour_package, name='delete_tour_package'),
]