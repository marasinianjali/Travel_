from rest_framework import generics
from social_community.models import Follow, DiscussionGroup, GroupPost, Tag, PostTag, Category, Post
from .serializers import (
    FollowSerializer, DiscussionGroupSerializer, GroupPostSerializer,
    TagSerializer, PostTagSerializer, CategorySerializer, PostSerializer
)
from rest_framework.permissions import IsAuthenticated

# Follow
class FollowListCreateView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

class FollowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

# DiscussionGroup
class DiscussionGroupListCreateView(generics.ListCreateAPIView):
    queryset = DiscussionGroup.objects.all()
    serializer_class = DiscussionGroupSerializer
    permission_classes = [IsAuthenticated]

class DiscussionGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscussionGroup.objects.all()
    serializer_class = DiscussionGroupSerializer
    permission_classes = [IsAuthenticated]

# GroupPost
class GroupPostListCreateView(generics.ListCreateAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

class GroupPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAuthenticated]

# Tag
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

# PostTag
class PostTagListCreateView(generics.ListCreateAPIView):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [IsAuthenticated]

class PostTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [IsAuthenticated]

# Category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Post
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
