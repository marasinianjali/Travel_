from django import forms
from .models import User, LoginAdmin, Wishlist, Trip, Notification
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import re

# Utility function to check for malicious input
def validate_input(value):
    pattern = r"[;'\"--]|(/\*.*\*/)|(<[^>]+>)"
    if re.search(pattern, value):
        raise ValidationError("Invalid or potentially harmful characters detected.")



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_input(username)
        return username


# User Signup Form
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'phone', 'address', 'gender', 'status', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'address', 'phone']:
            value = cleaned_data.get(field)
            if value:
                validate_input(value)
        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return make_password(password)


# User Login Form
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_input(email)
        return email


# Wishlist Form
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['destination_name', 'description']

    def __init__(self, *args, **kwargs):
        super(WishlistForm, self).__init__(*args, **kwargs)
        self.fields["destination_name"].required = True
        self.fields["description"].required = False

    def clean_destination_name(self):
        dest = self.cleaned_data.get('destination_name')
        validate_input(dest)
        return dest


# Trip Form
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_destination(self):
        destination = self.cleaned_data.get('destination')
        validate_input(destination)
        return destination


# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'address', 'bio', 'theme']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'theme': forms.Select(choices=[('light', 'Light'), ('dark', 'Dark')]),
        }
    

    def clean(self):
        cleaned_data = super().clean()
        for field in ['name', 'address', 'phone', 'bio']:
            value = cleaned_data.get(field)
            if value:
                validate_input(value)
        return cleaned_data


# Notification Form
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'notification_type']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
            'notification_type': forms.Select(choices=[('deal', 'Deal'), ('flight', 'Flight Change'), ('safety', 'Safety Update')]),
        }

    def clean_message(self):
        msg = self.cleaned_data.get('message')
        validate_input(msg)
        return msg


# User Registration Form (if used separately)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'phone', 'address', 'gender', 'status', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return make_password(password)
