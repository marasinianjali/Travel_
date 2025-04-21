from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from .models import Review
from .forms import ReviewForm
import os
from PIL import Image
from io import BytesIO
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

@csrf_protect
@login_required
def review_list(request):
    # Using select_related properly with specific fields
    reviews = Review.objects.select_related(
        'user', 'package', 'guide', 'hotel', 'company'
    ).only(
        'user__username', 'rating', 'review_text', 'created_at',
        'package__name', 'guide__name', 'hotel__name', 'company__name'
    ).order_by('-created_at')[:10]
    
    return render(request, 'review/review_list.html', {
        'reviews': reviews,
        'user': request.user  # Pass user to template for permission checks
    })

@csrf_protect
@transaction.atomic
@login_required
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.user = request.user
                
                # Process and validate image if uploaded
                if 'photo' in request.FILES:
                    review.photo = process_uploaded_image(request.FILES['photo'])
                
                review.save()
                messages.success(request, "Review submitted successfully!")
                return redirect('review:review_list')
            
            except Exception as e:
                messages.error(request, f"Error processing your review: {str(e)}")
                return render(request, 'review/add_review.html', {'form': form})
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm()
    
    return render(request, 'review/add_review.html', {
        'form': form,
        'allowed_image_types': ['image/jpeg', 'image/png']
    })

def process_uploaded_image(uploaded_image):
    """Process and validate uploaded images"""
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(uploaded_image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Only JPG, JPEG, and PNG are allowed.")
    
    # Check MIME type
    valid_mime_types = ['image/jpeg', 'image/png']
    if uploaded_image.content_type not in valid_mime_types:
        raise ValidationError("Unsupported file type. Only JPG and PNG are allowed.")
    
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if uploaded_image.size > max_size:
        raise ValidationError("File size too large. Maximum allowed is 5MB.")
    
    # Process image to prevent malicious files
    try:
        # Open the image using Pillow
        img = Image.open(uploaded_image)
        
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Create a BytesIO buffer
        img_io = BytesIO()
        
        # Save the image to the buffer
        img.save(img_io, format='JPEG' if ext in ['.jpg', '.jpeg'] else 'PNG', quality=85)
        
        # Create a new InMemoryUploadedFile
        new_image = InMemoryUploadedFile(
            img_io,
            'ImageField',
            uploaded_image.name,
            'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png',
            img_io.tell(),
            None
        )
        
        return new_image
        
    except Exception as e:
        raise ValidationError("Invalid image file. Please upload a valid image.")