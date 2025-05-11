from django.urls import path
from .api_views import (
     ArticleDetailView,
     TravelNewsDetailView,
     CommentDetailView, LikeDetailView
)

urlpatterns = [
    
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('travel-news/<int:pk>/', TravelNewsDetailView.as_view(), name='travel-news-detail'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('likes/<int:pk>/', LikeDetailView.as_view(), name='like-detail'),
]
