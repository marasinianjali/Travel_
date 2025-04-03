from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['package', 'guide', 'hotel', 'company', 'rating', 'review_text', 'photo']
