from rest_framework import serializers
from .models import Follow, DiscussionGroup, GroupPost, Tag, PostTag, Category, Post
from user_login.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email']

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'

class DiscussionGroupSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = DiscussionGroup
        fields = '__all__'

class GroupPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=DiscussionGroup.objects.all())

    class Meta:
        model = GroupPost
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
