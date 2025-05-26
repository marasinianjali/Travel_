from django.urls import path
from .api_views import  (
    FollowListCreateView, FollowDetailView, FollowDetailUserView,
    DiscussionGroupListCreateView, DiscussionGroupDetailView, DiscussionGroupDetailUserView,
    GroupPostListCreateView, GroupPostDetailView, GroupPostDetailUserView,
    TagListCreateView, TagDetailView, TagDetailUserView,
    PostTagListCreateView, PostTagDetailView, PostTagDetailUserView,
    CategoryListCreateView, CategoryDetailView, CategoryDetailUserView,
    PostListCreateView, PostDetailView, PostDetailUserView
)
app_name = 'social_community.api'

urlpatterns = [
    path('follows/', FollowListCreateView.as_view(), name='follow-list-create'),
    path('follows/<int:pk>/', FollowDetailView.as_view(), name='follow-detail'),
    path('user/follows/<int:pk>/', FollowDetailUserView.as_view(), name='follow-detail-user'),


    path('discussion-groups/', DiscussionGroupListCreateView.as_view(), name='group-list-create'),
    path('discussion-groups/<int:pk>/', DiscussionGroupDetailView.as_view(), name='group-detail'),
    path('user/discussion-groups/<int:pk>/', DiscussionGroupDetailUserView.as_view(), name='group-detail'),


    path('group-posts/', GroupPostListCreateView.as_view(), name='group-post-list-create'),
    path('group-posts/<int:pk>/', GroupPostDetailView.as_view(), name='group-post-detail'),
    path('user/group-posts/<int:pk>/', GroupPostDetailUserView.as_view(), name='group-post-detail'),

    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
    path('user/tags/<int:pk>/', TagDetailUserView.as_view(), name='tag-detail'),


    path('post-tags/', PostTagListCreateView.as_view(), name='post-tag-list-create'),
    path('post-tags/<int:pk>/', PostTagDetailView.as_view(), name='post-tag-detail'),
    path('user/post-tags/<int:pk>/', PostTagDetailUserView.as_view(), name='post-tag-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('user/categories/<int:pk>/', CategoryDetailUserView.as_view(), name='category-detail'),


    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/posts/<int:pk>/', PostDetailUserView.as_view(), name='post-detail'),
]
