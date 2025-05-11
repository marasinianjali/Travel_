from rest_framework import serializers
from .models import Article, TravelNews, Comment, Like
from social_community.models import Post, Category
from user_login.models import User


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


class TravelNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelNews
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True, required=False)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), allow_null=True, required=False)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Like
        fields = '__all__'
