from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.user_login.models import User
from apps.social_community.models import Post, Category
from .models import Article, TravelNews, Comment, Like
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator

def check_login(request):
    return "user_id" in request.session

# Home page
def travel_stories_home(request):
    posts = Post.objects.all().select_related('user', 'category')
    articles = Article.objects.all().select_related('author', 'category')
    news = TravelNews.objects.all()[:5]  # Limited to 5, no pagination needed

    # Pagination for posts
    posts_paginator = Paginator(posts, 10)  # 10 posts per page
    posts_page = request.GET.get('posts_page')
    try:
        posts_paginated = posts_paginator.page(posts_page)
    except PageNotAnInteger:
        posts_paginated = posts_paginator.page(1)
    except EmptyPage:
        posts_paginated = posts_paginator.page(posts_paginator.num_pages)

    # Pagination for articles
    articles_paginator = Paginator(articles, 10)  # 10 articles per page
    articles_page = request.GET.get('articles_page')
    try:
        articles_paginated = articles_paginator.page(articles_page)
    except PageNotAnInteger:
        articles_paginated = articles_paginator.page(1)
    except EmptyPage:
        articles_paginated = articles_paginator.page(articles_paginator.num_pages)

    context = {
        'posts': posts_paginated,
        'articles': articles_paginated,
        'news': news,
        'categories': Category.objects.all()
    }
    return render(request, 'social_stories/travel_stories_home.html', context)

# Category-wise content
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).select_related('user')
    articles = Article.objects.filter(category=category).select_related('author')

    # Pagination for posts
    posts_paginator = Paginator(posts, 10)  # 10 posts per page
    posts_page = request.GET.get('posts_page')
    try:
        posts_paginated = posts_paginator.page(posts_page)
    except PageNotAnInteger:
        posts_paginated = posts_paginator.page(1)
    except EmptyPage:
        posts_paginated = posts_paginator.page(posts_paginator.num_pages)

    # Pagination for articles
    articles_paginator = Paginator(articles, 10)  # 10 articles per page
    articles_page = request.GET.get('articles_page')
    try:
        articles_paginated = articles_paginator.page(articles_page)
    except PageNotAnInteger:
        articles_paginated = articles_paginator.page(1)
    except EmptyPage:
        articles_paginated = articles_paginator.page(articles_paginator.num_pages)

    return render(request, 'social_stories/category_detail.html', {
        'category': category,
        'posts': posts_paginated,
        'articles': articles_paginated
    })

# Author profile
def author_profile(request, user_id):
    author = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=author).select_related('user')
    articles = Article.objects.filter(author=author).select_related('author')

    # Pagination for posts
    posts_paginator = Paginator(posts, 10)  # 10 posts per page
    posts_page = request.GET.get('posts_page')
    try:
        posts_paginated = posts_paginator.page(posts_page)
    except PageNotAnInteger:
        posts_paginated = posts_paginator.page(1)
    except EmptyPage:
        posts_paginated = posts_paginator.page(posts_paginator.num_pages)

    # Pagination for articles
    articles_paginator = Paginator(articles, 10)  # 10 articles per page
    articles_page = request.GET.get('articles_page')
    try:
        articles_paginated = articles_paginator.page(articles_page)
    except PageNotAnInteger:
        articles_paginated = articles_paginator.page(1)
    except EmptyPage:
        articles_paginated = articles_paginator.page(articles_paginator.num_pages)

    return render(request, 'social_stories/author_profile.html', {
        'author': author,
        'posts': posts_paginated,
        'articles': articles_paginated
    })

# Post details and comments
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related('user')
    liked_user_ids = post.likes.values_list('user_id', flat=True)

    # Pagination for comments
    comments_paginator = Paginator(comments, 10)  # 10 comments per page
    comments_page = request.GET.get('comments_page')
    try:
        comments_paginated = comments_paginator.page(comments_page)
    except PageNotAnInteger:
        comments_paginated = comments_paginator.page(1)
    except EmptyPage:
        comments_paginated = comments_paginator.page(comments_paginator.num_pages)

    if request.method == 'POST' and check_login(request):
        user = get_object_or_404(User, id=request.session['user_id'])
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=user, post=post, content=content)
            messages.success(request, "Your comment has been added!")
        else:
            messages.error(request, "Comment cannot be empty.")
        return redirect('social_stories:post_detail', post_id=post_id)

    return render(request, 'social_stories/post_detail.html', {
        'post': post,
        'comments': comments_paginated,
        'liked_user_ids': liked_user_ids
    })

# Article details and comments
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all().select_related('user')
    liked_user_ids = article.likes.values_list('user_id', flat=True)

    # Pagination for comments
    comments_paginator = Paginator(comments, 10)  # 10 comments per page
    comments_page = request.GET.get('comments_page')
    try:
        comments_paginated = comments_paginator.page(comments_page)
    except PageNotAnInteger:
        comments_paginated = comments_paginator.page(1)
    except EmptyPage:
        comments_paginated = comments_paginator.page(comments_paginator.num_pages)

    if request.method == 'POST' and check_login(request):
        user = get_object_or_404(User, id=request.session['user_id'])
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=user, article=article, content=content)
            messages.success(request, "Your comment has been added!")
        else:
            messages.error(request, "Comment cannot be empty.")
        return redirect('social_stories:article_detail', article_id=article_id)

    return render(request, 'social_stories/article_detail.html', {
        'article': article,
        'comments': comments_paginated,
        'liked_user_ids': liked_user_ids
    })

# Like post

def like_post(request, post_id):
    user = get_object_or_404(User, id=request.session['user_id'])
    post = get_object_or_404(Post, id=post_id)

    like_obj = Like.objects.filter(user=user, post=post)
    if like_obj.exists():
        like_obj.delete()
        messages.success(request, "You unliked this post.")
    else:
        Like.objects.create(user=user, post=post)
        messages.success(request, "You liked this post!")

    return redirect('social_stories:post_detail', post_id=post_id)

# Like article
@login_required
def like_article(request, article_id):
    user = get_object_or_404(User, id=request.session['user_id'])
    article = get_object_or_404(Article, id=article_id)

    like_obj = Like.objects.filter(user=user, article=article)
    if like_obj.exists():
        like_obj.delete()
        messages.success(request, "You unliked this article.")
    else:
        Like.objects.create(user=user, article=article)
        messages.success(request, "You liked this article!")

    return redirect('social_stories:article_detail', article_id=article_id)

# Add comment to post
@login_required
def add_comment_to_post(request, post_id):
    if not check_login(request):
        messages.error(request, "Please log in to comment.")
        return redirect('user-login')
    
    post = get_object_or_404(Post, id=post_id)
    user = User.objects.get(id=request.session['user_id'])
    content = request.POST.get('content')

    if content:
        Comment.objects.create(user=user, post=post, content=content)
        messages.success(request, "Your comment has been added!")

    return redirect('social_stories:post_detail', post_id=post_id)

# Add comment to article
@login_required
def add_comment_to_article(request, article_id):
    if not check_login(request):
        messages.error(request, "Please log in to comment.")
        return redirect('user-login')
    
    article = get_object_or_404(Article, id=article_id)
    user = User.objects.get(id=request.session['user_id'])
    content = request.POST.get('content')

    if content:
        Comment.objects.create(user=user, article=article, content=content)
        messages.success(request, "Your comment has been added!")

    return redirect('social_stories:article_detail', article_id=article_id)

# Edit comment
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.session.get('user_id') != comment.user.id:
        messages.error(request, "You can only edit your own comments.")
        return redirect('social_stories:post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        comment.content = content
        if image:
            comment.image = image
        comment.save()
        messages.success(request, "Comment updated successfully!")
        return redirect('social_stories:post_detail', post_id=comment.post.id)

    return render(request, 'social_stories/edit_comment.html', {'comment': comment})

# Delete comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.session.get('user_id') != comment.user.id:
        messages.error(request, "You can only delete your own comments.")
        return redirect('social_stories:post_detail', post_id=comment.post.id)

    post_id = comment.post.id
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('social_stories:post_detail', post_id=post_id)