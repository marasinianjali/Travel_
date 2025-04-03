# forms.py

from django import forms
from .models import Booking
from hotelbooking.models import HotelBooking
from tour_package.models import TourPackage
from Guides.models import Guide

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'hotel', 'user_name', 'phone_number', 'total_members', 
            'package', 'guide', 'booking_date', 'booking_details', 'status', 
            'promecode', 'pickup_location'
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }
