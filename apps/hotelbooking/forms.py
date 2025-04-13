from django import forms
from .models import HotelRoom, HotelRevenue, RoomAvailability, HotelBooking,HotelReport
from django.contrib.auth.models import User
from datetime import date

# Hotel Booking Form
class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['hotel_name', 'amount', 'room_type', 'photo', 'hotel_address', 
                  'contact_number', 'total_person', 'arrive_time', 'checkout_time', 
                   'total_price', 'location', 'latitude', 'longitude', 'email','amenity','rooms_available','notify_admin','status']

# Hotel Room Form
class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = '__all__'

# Hotel Revenue Filter/Edit Form
class HotelRevenueFilterForm(forms.ModelForm):
    class Meta:
        model = HotelRevenue
        fields='__all__'
# Hotel Amenities Form

# Room Availability Form
class RoomAvailabilityForm(forms.ModelForm):
    class Meta:
        model = RoomAvailability
        fields = '__all__'
        widgets = {
            'available_date': forms.DateInput(attrs={'type': 'date'}),  # Adding a date picker
        }

    # Example of adding custom validation to the form level
    def clean_available_date(self):
        available_date = self.cleaned_data.get('available_date')
        if available_date and available_date < date.today():
            raise forms.ValidationError("Availability date cannot be in the past.")
        return available_date
# Hotel Login Form


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError('Username does not exist.')
        return username
    
class HotelReportForm(forms.ModelForm):
    class Meta:
        model = HotelReport
        fields = ['hotel_booking', 'report_type', 'report_date', 'report_data']

    def clean_report_data(self):
        data = self.cleaned_data.get('report_data')
        if not data:
            raise forms.ValidationError("Report data cannot be empty.")
        return data


class HotelReportForm(forms.ModelForm):
    class Meta:
        model = HotelReport
        fields = ['hotel_booking', 'report_type', 'report_date', 'report_data']

    def clean_report_data(self):
        data = self.cleaned_data.get('report_data')
        if not data:
            raise forms.ValidationError("Report data cannot be empty.")
        return data
