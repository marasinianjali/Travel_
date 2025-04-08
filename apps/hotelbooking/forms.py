from django import forms
from .models import HotelBooking,HotelRoom,HotelRevenue

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = '__all__'
class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = '__all__'  # replace with actual fields

class HotelRevenueFilterForm(forms.ModelForm):
    class Meta:
        model = HotelRevenue
        fields = '__all__'
