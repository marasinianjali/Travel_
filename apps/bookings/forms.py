from django import forms
from django.core.exceptions import ValidationError
from .models import Booking
from apps.hotelbooking.models import HotelBooking
from apps.tour_package.models import TourPackage
from apps.Guides.models import Guide
from datetime import date


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'hotel', 'user_name', 'phone_number', 'total_members',
            'package', 'guide', 'booking_date', 'booking_details', 'status',
            'promecode', 'pickup_location'
        ]
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'total_members': forms.NumberInput(attrs={'min': 1}),
            'booking_details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Additional details'}),
            'promecode': forms.TextInput(attrs={'placeholder': 'Enter promo code'}),
            'pickup_location': forms.TextInput(attrs={'placeholder': 'Enter pickup location'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if booking_date < date.today():
            raise ValidationError("Booking date cannot be in the past.")
        return booking_date

    def clean_total_members(self):
        total_members = self.cleaned_data['total_members']
        if total_members <= 0:
            raise ValidationError("Total members must be greater than zero.")
        return total_members

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.replace('+', '').replace('-', '').isdigit():
            raise ValidationError("Phone number must contain only digits, +, or -.")
        return phone_number