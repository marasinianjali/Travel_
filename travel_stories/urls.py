from django.urls import path
from . import views

app_name = 'travel_stories'

urlpatterns = [
    path('', views.travel_stories_home, name='travel_stories_home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('author/<int:user_id>/', views.author_profile, name='author_profile'),
    path('post/<int:post_id>/', views.post_details, name='post_detail'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('article/<int:article_id>/like/', views.like_article, name='like_article'),
    path('post/<int:post_id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('article/<int:article_id>/comment/', views.add_comment_to_article, name='add_comment_to_article'),
]