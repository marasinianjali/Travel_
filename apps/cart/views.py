
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.contrib.contenttypes.models import ContentType

class AddToCartView(APIView):
    def post(self, request):
        user = request.user if request.user.is_authenticated else None
        item_type = request.data.get('item_type')  # E.g., 'tourpackage', 'hotel', 'guide'
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)

        # Map item_type to model
        model_map = {
            'tourpackage': ('tour_package', 'TourPackage'),
            'hotel': ('hotelbooking', 'Hotel'),
            'guide': ('Guides', 'Guide')
        }
        if item_type not in model_map:
            return Response({"error": "Invalid item type"}, status=status.HTTP_400_BAD_REQUEST)

        # Get ContentType
        app_label, model_name = model_map[item_type]
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
        except ContentType.DoesNotExist:
            return Response({"error": "Item type not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify item exists
        if not content_type.model_class().objects.filter(id=item_id).exists():
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create cart
        cart, _ = Cart.objects.get_or_create(user=user)
        CartItem.objects.create(
            cart=cart,
            content_type=content_type,
            object_id=item_id,
            quantity=quantity
        )

        return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)

class CartView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        try:
            cart = Cart.objects.get(user=user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"items": []}, status=status.HTTP_200_OK)

class RemoveFromCartView(APIView):
    def delete(self, request, item_id):
        user = request.user if request.user.is_authenticated else None
        try:
            cart = Cart.objects.get(user=user)
            cart_item = cart.items.get(id=item_id)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({"error": "Item or cart not found"}, status=status.HTTP_404_NOT_FOUND)
