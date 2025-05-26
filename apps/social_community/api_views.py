from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from social_community.models import Follow, DiscussionGroup, GroupPost, Tag, PostTag, Category, Post
from .serializers import (
    FollowSerializer, DiscussionGroupSerializer, GroupPostSerializer,
    TagSerializer, PostTagSerializer, CategorySerializer, PostSerializer
)
from .permissions import IsUser, IsAdmin

from rest_framework.permissions import IsAuthenticated

# Follow
class FollowListCreateView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAdmin]

class FollowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAdmin]

# Follow by user
class FollowDetailUserView(generics.RetrieveAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsUser]

# DiscussionGroup
class DiscussionGroupListCreateView(generics.ListCreateAPIView):
    queryset = DiscussionGroup.objects.all()
    serializer_class = DiscussionGroupSerializer
    permission_classes = [IsAdmin]

class DiscussionGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscussionGroup.objects.all()
    serializer_class = DiscussionGroupSerializer
    permission_classes = [IsAdmin]

# DiscussionGroup by user
class DiscussionGroupDetailUserView(generics.RetrieveAPIView):
    queryset = DiscussionGroup.objects.all()
    serializer_class = DiscussionGroupSerializer
    permission_classes = [IsUser]

# GroupPost
class GroupPostListCreateView(generics.ListCreateAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAdmin]

class GroupPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsAdmin]

# GroupPost by user
class GroupPostDetailUserView(generics.RetrieveAPIView):
    queryset = GroupPost.objects.all()
    serializer_class = GroupPostSerializer
    permission_classes = [IsUser]


# Tag
class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdmin]

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdmin]

# Tag by user
class TagDetailUserView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsUser]


# PostTag
class PostTagListCreateView(generics.ListCreateAPIView):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [IsAdmin]

class PostTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [IsAdmin]

# PostTag by user
class PostTagDetailUserView(generics.RetrievAPIView):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [IsUser]

# Category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

# Category by user
class CategoryDetailUserView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsUser]


# Post
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdmin]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdmin]

# Post by user
class PostDetailUserView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsUser]
