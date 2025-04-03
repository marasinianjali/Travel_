from django import forms
from user_login.models import User
from .models import Post

class FollowUserForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Enter username to follow'})
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows':4, 'placeholder': 'share your story or experience.....'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'accept': 'video/*'}),
            'category': forms.Select(),

        }
        labels = {
            'content': 'Your Post',
            'image': 'Upload Image',
            'category': 'Category',
        }