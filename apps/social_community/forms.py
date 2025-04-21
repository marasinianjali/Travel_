from django import forms
from apps.user_login.models import User
from .models import Post
from django.core.exceptions import ValidationError
import os

class FollowUserForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Enter username to follow'})
    )



class PostForm(forms.ModelForm):
    MAX_IMAGE_SIZE_MB = 5
    MAX_VIDEO_SIZE_MB = 50
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in self.ALLOWED_IMAGE_EXTENSIONS:
                raise ValidationError("Allowed image formats: JPG, JPEG, PNG.")
            if image.size > self.MAX_IMAGE_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"Max image size is {self.MAX_IMAGE_SIZE_MB}MB.")
        return image

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            ext = os.path.splitext(video.name)[1].lower()
            if ext not in self.ALLOWED_VIDEO_EXTENSIONS:
                raise ValidationError("Allowed video formats: MP4, MOV, AVI, MKV.")
            if video.size > self.MAX_VIDEO_SIZE_MB * 1024 * 1024:
                raise ValidationError(f"Max video size is {self.MAX_VIDEO_SIZE_MB}MB.")
        return video

    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'placeholder': 'share your story or experience.....'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'accept': 'video/*'}),
            'category': forms.Select(),
        }
