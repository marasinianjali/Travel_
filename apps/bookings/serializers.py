from rest_framework import serializers
from . models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'user', 'hotel', 'user_name',
            'phone_number', 'total_members', 'package',
            'guide', 'booking_date', 'booking_details',
            'status'
        ]

        read_only_fields = ['booking_id']  # Make booking_id read-only
        extra_kwargs = {
            'user_name': {'required': True},
            'phone_number': {'required': True},
            'total_members': {'required': True},
            'package': {'required': True},
            'booking_date': {'required': True}
        }