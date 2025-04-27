from django.db import models
from django.contrib.auth.models import User
from apps.user_login.models import User
from fernet_fields import EncryptedCharField, EncryptedTextField, EncryptedDateTimeField

class Follow(models.Model):
    follower = models.ForeignKey('user_login.User', related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey('user_login.User', related_name='followed', on_delete=models.CASCADE)
    created_at = EncryptedDateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.name} follows {self.followed.name}"
    
    class Meta:
        unique_together = ('follower', 'followed')
        db_table = 'follows'  # Tell Django to use the existing 'follows' table



class DiscussionGroup(models.Model):
    name = EncryptedCharField(max_length=255)
    description = EncryptedTextField(blank=True, null=True)
    created_by = models.ForeignKey('user_login.User', on_delete=models.CASCADE)
    content = EncryptedTextField()
    created_at = EncryptedDateTimeField(auto_now_add=True)

    class Meta:
        
        db_table = 'discussion_groups'  # Tell Django to use the existing 'follows' table


class GroupPost(models.Model):
    group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE)
    user = models.ForeignKey('user_login.User', on_delete=models.CASCADE)
    content = EncryptedTextField()
    created_at = EncryptedDateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = EncryptedCharField(max_length=100)
    created_at = EncryptedDateTimeField(auto_now_add=True)

class PostTag(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = EncryptedDateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'tag')

class Category(models.Model):
    name = EncryptedCharField(max_length=100)
    description = EncryptedTextField(blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'categories'


class Post(models.Model):
    # group = models.ForeignKey('social_community.DiscussionGroup', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = EncryptedTextField()
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = EncryptedDateTimeField(auto_now_add=True)
    updated_at = EncryptedDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] #Newest posts first 
        db_table = 'group_posts'

    def __str__(self):
        return f"Post by {self.user.name} on {self.created_at}"

