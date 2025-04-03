from django.db import models
from user_login.models import User
from social_community.models import Category 

class Article(models.Model):
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/images', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class TravelNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('social_community.Post', related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'article')

    def __str__(self):
        return f"Like by {self.user.name} on {self.created_at}"
    
class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey('social_community.Post', related_name='likes', on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post', 'article')

    def __str__(self):
        return f"Like by {self.user.name} on {self.created_at}"