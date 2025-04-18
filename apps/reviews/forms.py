from django import forms
from django.core.exceptions import ValidationError
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['package', 'guide', 'hotel', 'company', 'rating', 'review_text', 'photo']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'guide': forms.Select(attrs={'class': 'form-control'}),
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        package = cleaned_data.get('package')
        guide = cleaned_data.get('guide')
        hotel = cleaned_data.get('hotel')
        company = cleaned_data.get('company')

        if not (package or guide or hotel or company):
            raise ValidationError("At least one of Package, Guide, Hotel, or Company must be selected.")

        return cleaned_data

    def clean_review_text(self):
        review_text = self.cleaned_data['review_text']
        if review_text and len(review_text.strip()) < 10:
            raise ValidationError("Review text must be at least 10 characters long if provided.")
        return review_text



