from decimal import Decimal
from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import Guide
from django.contrib.auth.forms import UserCreationForm
 # Make sure UserBase is your custom user model

class GuideForm(forms.ModelForm):
    # Custom fields
    phone_number = forms.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        
        max_length=254,
        validators=[EmailValidator()],
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Guide
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'about_us': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'languages': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'expertise': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.startswith('+') and not phone.isdigit():
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if experience < 0 or experience > 60:
            raise forms.ValidationError("Experience must be between 0 and 60 years.")
        return experience

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0.0 or rating > 5.0:
            raise forms.ValidationError("Rating must be between 0.0 and 5.0.")
        return rating

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', "Guides")
        super().__init__(*args, **kwargs)

        if user_role == "Guides" and 'is_approved' in self.fields:
            self.fields['is_approved'].disabled = True
            self.fields['is_approved'].widget.attrs['readonly'] = True

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None:
            try:
                decimal_amount = Decimal(str(amount))
                if decimal_amount < Decimal('0.00'):
                    raise forms.ValidationError("Amount must be a positive number.")
                return decimal_amount  # Return Decimal, not string
            except (ValueError, TypeError):
                raise forms.ValidationError("Invalid amount format.")
        return amount