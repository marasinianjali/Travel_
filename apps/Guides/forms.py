from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import Guide

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
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'languages': forms.SelectMultiple(attrs={'class': 'form-control'}),  # Change to SelectMultiple for dropdown
            'about_us': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'expertise': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0 or rating > 5:
            raise forms.ValidationError("Rating must be between 0.0 and 5.0.")
        return rating

    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if experience < 0 or experience > 60:
            raise forms.ValidationError("Experience must be between 0 and 60.")
        return experience
