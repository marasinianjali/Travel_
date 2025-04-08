from django import forms
from .models import TourismCompany
from django.contrib.auth.forms import AuthenticationForm

class TourismCompanyForm(forms.ModelForm):
    class Meta:
        model = TourismCompany
        fields = [
            'user_name', 'user_phone', 'user_email', 
            'company_name', 'company_phone', 'company_address'
        ]

#This is for the company signup form 
class CompanySignupForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = TourismCompany
        fields = [ 'company_name', 'company_phone', 'company_address']

#this is for company to login 
class CompanyLoginForm(forms.Form):
    company_name = forms.CharField(label="Company Name", max_length=255)
    # company_phone = forms.CharField(label="Company Phone", max_length=255)
    # company_address = forms.CharField(label="Company Address", max_length=255)