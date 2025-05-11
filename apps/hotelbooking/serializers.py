from rest_framework import serializers
from.models import HotelBooking, HotelRevenue
from django.contrib.auth.models import User
class HotelBookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    location = serializers.StringRelatedField()

    class Meta:
        model = HotelBooking
        fields = '__all__'

class HotelRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRevenue
        fields = '__all__'
