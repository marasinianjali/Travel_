from django import forms
from django.core.exceptions import ValidationError
from .models import Review
import os

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['package', 'guide', 'hotel', 'company', 'rating', 'review_text', 'photo']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here (minimum 10 characters)',
                'class': 'form-control'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/jpeg, image/png'
            }),
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

        if not any([package, guide, hotel, company]):
            raise ValidationError("At least one of Package, Guide, Hotel, or Company must be selected.")

        return cleaned_data

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text', '').strip()
        if review_text and len(review_text) < 10:
            raise ValidationError("Review text must be at least 10 characters long if provided.")
        return review_text

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(photo.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file extension. Only JPG, JPEG, and PNG are allowed.")
            
            # Check content type
            valid_mime_types = ['image/jpeg', 'image/png']
            if hasattr(photo, 'content_type') and photo.content_type not in valid_mime_types:
                raise ValidationError("Unsupported file type. Only JPG and PNG are allowed.")
            
            # Check file size (max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB
            if photo.size > max_size:
                raise ValidationError("File size too large. Maximum allowed is 5MB.")
        
        return photo