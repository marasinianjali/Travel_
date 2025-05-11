from rest_framework import serializers
from apps.user_login.models import User, Wishlist, Trip, Notification, Booking, Guide, Language, LoginAdmin
from apps.tour_package.models import TourPackage  # Adjust if it's not correct

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']  # or use write_only=True for password

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'

class LoginAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAdmin
        exclude = ['password']
