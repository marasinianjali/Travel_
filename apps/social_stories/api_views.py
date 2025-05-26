from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions
from .models import Article, TravelNews, Comment, Like
from .serializers import ArticleSerializer, TravelNewsSerializer, CommentSerializer, LikeSerializer

from .permissions import IsAdminOrIsUser, IsUser, IsAdmin


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrIsUser]

class TravelNewsDetailView(generics.RetrieveAPIView):
    queryset = TravelNews.objects.all()
    serializer_class = TravelNewsSerializer
    permission_classes = [IsAdminOrIsUser]

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsUser]

# For to read only for Admin
class CommentDetailAdminView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdmin]



class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsUser]

class LikeDetailAdminView(generics.RetrieveAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAdmin]
