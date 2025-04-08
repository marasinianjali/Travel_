from django import forms
from .models import TourPackage
from datetime import date

class TourPackageForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
        label="Select Date"
    )

    class Meta:
        model = TourPackage
        fields = '__all__'  # Includes all fields

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)  # Get user role from kwargs
        super(TourPackageForm, self).__init__(*args, **kwargs)
        
        # Disable "is_approved" if the user is a Tourism Company
        if user_role == "TourismCompany":
            self.fields['is_approved'].disabled = True
            self.fields['is_approved'].widget.attrs['readonly'] = True  # Make it non-editable
