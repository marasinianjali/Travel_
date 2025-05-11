from rest_framework import generics, permissions
from .models import Article, TravelNews, Comment, Like
from .serializers import ArticleSerializer, TravelNewsSerializer, CommentSerializer, LikeSerializer


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]
class TravelNewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TravelNews.objects.all()
    serializer_class = TravelNewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
