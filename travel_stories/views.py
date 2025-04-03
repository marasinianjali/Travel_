from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user_login.models import User
from social_community.models import Post, Category
from .models import Article, TravelNews, Comment, Like

def check_login(request):
    if "user_id" not in request.session:
        return False
    return True
def travel_stories_home(request):
    posts = Post.objects.all().select_related('user', 'category')
    articles = Article.objects.all().select_related('author', 'category')
    news = TravelNews.objects.all()[:5] #Latest 5 news updates
    categories = Category.objects.all()

    return render(request, 'travel_stories/travel_stories_home.html', {
        'posts': posts,
        'articles': articles,
        'news': news,
        'categories': categories,
    })

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).select_related('user')
    articles = Article.objects.filter(category=category).select_related('author')

    return render(request, 'travel_stories/category_detail.html', {
        'category': category,
        'posts': posts,
        'articles': articles, 
    })

def author_profile(request, user_id):
    author = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=author).select_related('user')
    articles = Article.objects.filter(author=author).select_related('author')

    return render(request, 'travel_stories/author_profile.html', {
        'author': author,
        'posts': posts,
        'articles': articles,
    })

def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related('user')

    # Get the list of user IDs who liked this post
    liked_user_ids = post.likes.values_list('user_id', flat=True)
    
    if request.method == 'POST' and check_login(request):
        user = User.objects.get(id=request.session['user_id'])
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=user, post=post, content=content)
            messages.success(request, "Your comment has been added!")
            return redirect('travel_stories:post_detail', post_id=post_id)
        else:
            messages.error(request, "Comment cannot be empty.")
            return redirect('travel_stories:post_detail', post_id=post_id)

    return render(request, 'travel_stories/post_detail.html', {
        'post': post,
        'comments': comments,
        'liked_user_ids': liked_user_ids, # Pass the llist of user IDs to the template
    })


# def article_detail(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     comments = article.comments.all().select_related('user')

#     # Get the list of user IDs who liked this article
#     liked_user_ids = article.likes.values_list('user_id', flat=True)
    
#     if request.method == 'POST' and check_login(request):
#         user= User.objects.get(id=request.session['user_id'])
#         post = get_object_or_404(Post, id=post_id)

#         if Like.objects.filter(user=user, post=post).exists():
#             Like.objects.filter(user=user, post=post).delete()
#             messages.success(request, "You unliked this post.")
#         else:
#             Like.objects.create(user=user, post=post)
#             messages.success(request, "You liked this post!")

#         return redirect('travel_stories:post_detail', post_id=post_id)

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all().select_related('user')
    
    # Get the list of user IDs who liked this article
    liked_user_ids = article.likes.values_list('user_id', flat=True)
    
    if request.method == 'POST' and check_login(request):
        user = User.objects.get(id=request.session['user_id'])
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=user, article=article, content=content)
            messages.success(request, "Your comment has been added!")
            return redirect('travel_stories:article_detail', article_id=article_id)
        else:
            messages.error(request, "Comment cannot be empty.")
            return redirect('travel_stories:article_detail', article_id=article_id)
    
    return render(request, 'travel_stories/article_detail.html', {
        'article': article,
        'comments': comments,
        'liked_user_ids': liked_user_ids,  # Pass the list of user IDs to the template
    })

def like_post(request, post_id):
    if not check_login(request):
        messages.error(request, "Please log in to like a post.")
        return redirect('user-login')
    
    user = User.objects.get(id=request.session['user_id'])
    post = get_object_or_404(Post, id=post_id)

    if Like.objects.filter(user=user, post=post).exists():
        Like.objects.filter(user=user, post=post).delete()
        messages.success(request, "Your unliked this post.")
    else:
        Like.objects.create(user=user, post=post)
        messages.success(request, "You liked this post!")

    return redirect('travel_stories:post_detail', post_id=post_id)


def like_article(request, article_id):
    if not check_login(request):
        messages.error(request, "Please log in to like an article.")
        return redirect('user-login')
    
    user = User.objects.get(id=request.session['user_id'])
    article = get_object_or_404(Article, id=article_id)

    if Like.objects.filter(user=user, article=article).exists():
        Like.objects.filter(user=user, article=article).delete()
        messages.success(request, "You unliked this article.")
    else:
        Like.objects.create(ser=user, article=article)
        messages.success(request, "You liked this articles!")
    return redirect('travel_stories:article_detail', article_id=article_id)

def add_comment_to_post(request, post_id):
    if not check_login(request):
        messages.error(request, "Please log in to comment.")
        return redirect('user-login')
    
    post = get_object_or_404(post, id=post_id)
    user = User.objects.get(id=request.session['user_id'])
    content = request.POST.get('content')

    if content:
        Comment.objects.create(user=user, post=post, content=content)
        messages.success(request, "Your comment has been added!")

    return redirect('travel_stories:post_detail', post_id=post_id)

def add_comment_to_article(request, article_id):
    if not check_login(request):
        messages.error(request, "Please log in to comment.")
        return redirect('user-login')
    
    article = get_object_or_404(Article, id=article_id)
    user = User.objects.get(id=request.session['user_id'])
    content = request.POST.get('content')

    if content:
        Comment.objects.create(user=user, article=article, content=content)
        messages.success(request, "Your comment has beed added!")

    return redirect('travel_stories:article_detail', article_id=article_id)
