from django import forms
from .models import HotelRoom, HotelRevenue, RoomAvailability, HotelBooking, HotelReport
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

# -------------------------
# Hotel Booking Form
# -------------------------
class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = [
            'hotel_name', 'amount', 'room_type', 'photo', 'hotel_address',
            'contact_number', 'total_person', 'arrive_time', 'checkout_time',
            'total_price', 'location', 'latitude', 'longitude', 'email',
            'amenity', 'rooms_available', 'notify_admin', 'status'
        ]

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and not photo.content_type in ['image/jpeg', 'image/png']:
            raise ValidationError('Only JPEG and PNG files are allowed.')
        return photo

    def clean_arrive_time(self):
        arrive_time = self.cleaned_data.get('arrive_time')
        if arrive_time and arrive_time < date.today():
            raise ValidationError("Arrival time cannot be in the past.")
        return arrive_time

    def clean_checkout_time(self):
        arrive_time = self.cleaned_data.get('arrive_time')
        checkout_time = self.cleaned_data.get('checkout_time')
        if arrive_time and checkout_time and checkout_time <= arrive_time:
            raise ValidationError("Checkout time must be after arrival time.")
        return checkout_time


# -------------------------
# Hotel Room Form
# -------------------------
class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = '__all__'


# -------------------------
# Hotel Revenue Filter/Edit Form
# -------------------------
class HotelRevenueFilterForm(forms.ModelForm):
    class Meta:
        model = HotelRevenue
        fields = '__all__'


# -------------------------
# Room Availability Form
# -------------------------
class RoomAvailabilityForm(forms.ModelForm):
    class Meta:
        model = RoomAvailability
        fields = '__all__'
        widgets = {
            'available_date': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_available_date(self):
        available_date = self.cleaned_data.get('available_date')
        if available_date and available_date < date.today():
            raise forms.ValidationError("Availability date cannot be in the past.")
        return available_date


# -------------------------
# Hotel Login Form
# -------------------------
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError('Username does not exist.')
        return username


# -------------------------
# Hotel Report Form
# -------------------------
class HotelReportForm(forms.ModelForm):
    class Meta:
        model = HotelReport
        fields = ['hotel_booking', 'report_type', 'report_date', 'report_data']

    def clean_report_data(self):
        data = self.cleaned_data.get('report_data')
        if not data:
            raise forms.ValidationError("Report data cannot be empty.")
        return data

    def clean_report_date(self):
        report_date = self.cleaned_data.get('report_date')
        if report_date and report_date > date.today():
            raise ValidationError("Report date cannot be in the future.")
        return report_date
