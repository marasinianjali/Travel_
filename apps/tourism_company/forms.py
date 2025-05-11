from django import forms
from .models import TourismCompany


class TourismCompanyForm(forms.ModelForm):
    class Meta:
        model = TourismCompany
        fields = [
            'user_name', 'user_phone', 'user_email',
            'company_name', 'company_phone', 'company_address'
        ]
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TourismCompanyCreateForm(forms.ModelForm):
    class Meta:
        model = TourismCompany
        fields = ['company_name', 'company_phone', 'company_address']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CompanySignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )

    class Meta:
        model = TourismCompany
        fields = ['company_name', 'company_phone', 'company_address', 'password']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CompanyLoginForm(forms.Form):
    company_name = forms.CharField(
        label="Company Name",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
  
