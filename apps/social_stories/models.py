from django.db import models
from apps.user_login.models import User
from apps.social_community.models import Category, Post
from fernet_fields import EncryptedCharField, EncryptedTextField, EncryptedDateTimeField



class Article(models.Model):
    author = models.ForeignKey(
        User,
        related_name='articles',
        on_delete=models.CASCADE,
        verbose_name="Author",
        help_text="User who wrote the article."
    )
    title = EncryptedCharField(
        max_length=200,
        verbose_name="Title",
        help_text="Title of the article."
    )
    content = EncryptedTextField(
        verbose_name="Content",
        help_text="Main content of the article."
    )
    image = models.ImageField(
        upload_to='articles/images',
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Optional image for the article."
    )
    category = models.ForeignKey(
        Category,
        related_name='articles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Category",
        help_text="Category of the article."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the article was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Timestamp when the article was last updated."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table = "article_article"

    def __str__(self):
        return self.title


class TravelNews(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        help_text="Title of the travel news."
    )
    content = models.TextField(
        verbose_name="Content",
        help_text="Content of the travel news."
    )
    source = models.URLField(
        blank=True,
        null=True,
        verbose_name="Source URL",
        help_text="Optional source link of the news."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the news was published."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Travel News"
        verbose_name_plural = "Travel News"
        db_table = "article_travelnews"

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="User who made the comment."
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Post",
        help_text="Post on which the comment was made."
    )
    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Article",
        help_text="Article on which the comment was made."
    )
    image = models.ImageField(
        upload_to='comment_images/',
        null=True,
        blank=True,
        verbose_name="Comment Image",
        help_text="Optional image for the comment."
    )
    content = models.TextField(
        verbose_name="Content",
        help_text="Content of the comment."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the comment was made."
    )

    class Meta:
        unique_together = ('user', 'post', 'article')
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        db_table = "article_comment"

    def __str__(self):
        return f"Comment by {self.user.name} on {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="User who liked the post or article."
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Post",
        help_text="Post that was liked."
    )
    article = models.ForeignKey(
        Article,
        related_name='likes',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Article",
        help_text="Article that was liked."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the like was made."
    )

    class Meta:
        unique_together = ('user', 'post', 'article')
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        db_table = "article_like"

    def __str__(self):
        return f"Like by {self.user.name} on {self.created_at}"
