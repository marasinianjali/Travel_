from django import forms
from .models import User, LoginAdmin
from django.contrib.auth.hashers import check_password  # For secure password checking
from django.contrib.auth.hashers import make_password
from .models import User, Wishlist, Trip, Notification

# Admin Login Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginAdmin
        fields = ['username', 'password']

# User Signup Form

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'phone', 'address', 'gender', 'status', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),  # Ensure correct input type
            'password': forms.PasswordInput(),  # Hide password input
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)  # Hash password before saving

   

# User Login Form
class UserLoginForm(forms.Form):  # Use Form, not ModelForm
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



# Form for Adding to Wishlist
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['destination_name', 'description']
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 3}),
        # }
        
    def __init__(self, *args, **kwargs):
        super(WishlistForm, self).__init__(*args, **kwargs)
        self.fields["destination_name"].required = True
        self.fields["description"].required = False  # Make it optional
        

# Form for Adding a Trip
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Form for Updating Profile Customization
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'address', 'bio', 'theme']  # Add fields you want users to edit
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'theme': forms.Select(choices=[('light', 'Light'), ('dark', 'Dark')]),
        }

# Optional: Form for Manual Notification Creation 
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'notification_type']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
            'notification_type': forms.Select(choices=[('deal', 'Deal'), ('flight', 'Flight Change'), ('safety', 'Safety Update')]),
        }



# User Registration Form
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
        return password  # Ideally, hash the password before saving
