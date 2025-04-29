# cart/urls.py
from django.urls import path
from .views import AddToCartView, CartView, RemoveFromCartView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('', CartView.as_view(), name='view_cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]