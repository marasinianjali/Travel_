from django.shortcuts import render, redirect, get_object_or_404
from apps.user_login.models import User
from .models import Follow, Post
from django.contrib import messages
from .forms import PostForm
from django.db.models import Q
from django.utils.html import escape
from apps.social_community.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import Paginator

Category.objects.all()

def check_login(request):
    if "user_id" not in request.session:
        return False
    return True

def followed_list(request):
    if not check_login(request):
        return redirect("user-login")

    user = User.objects.get(id=request.session["user_id"])
    search_query = request.GET.get('search', '').strip()

    followed = Follow.objects.filter(follower=user).select_related('followed')

    if search_query:
        safe_query = escape(search_query)
        followed = followed.filter(Q(followed__name__icontains=safe_query))

    # Pagination
    paginator = Paginator(followed, 10)  # Show 10 followed users per page
    page = request.GET.get('page')
    try:
        followed_page = paginator.page(page)
    except PageNotAnInteger:
        followed_page = paginator.page(1)
    except EmptyPage:
        followed_page = paginator.page(paginator.num_pages)

    return render(request, 'social_community/following_list.html', {
        'followed': followed_page,  # Pass paginated object
        'search_query': search_query,
    })

def followers_list(request):
    if not check_login(request):
        return redirect("user-login")

    user = User.objects.get(id=request.session["user_id"])
    followers = Follow.objects.filter(followed=user).select_related('follower')

    # Pagination
    paginator = Paginator(followers, 10)  # Show 10 followers per page
    page = request.GET.get('page')
    try:
        followers_page = paginator.page(page)
    except PageNotAnInteger:
        followers_page = paginator.page(1)
    except EmptyPage:
        followers_page = paginator.page(paginator.num_pages)

    return render(request, 'social_community/followers_list.html', {
        'followers': followers_page,  # Pass paginated object
    })

def public_profile(request, user_id):
    if not check_login(request):
        return redirect("user-login")

    current_user = User.objects.get(id=request.session["user_id"])
    profile_user = get_object_or_404(User, id=user_id)

    followed_count = Follow.objects.filter(follower=profile_user).count()
    followers_count = Follow.objects.filter(followed=profile_user).count()
    is_following = Follow.objects.filter(follower=current_user, followed=profile_user).exists()

    posts = Post.objects.filter(user=profile_user).select_related('user')

    # Pagination for posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    if request.method == 'POST' and 'follow_user' in request.POST:
        if profile_user == current_user:
            messages.error(request, "You cannot follow yourself!")
        else:
            if is_following:
                Follow.objects.filter(follower=current_user, followed=profile_user).delete()
                messages.success(request, f"You have unfollowed {profile_user.name}.")
            else:
                Follow.objects.create(follower=current_user, followed=profile_user)
                messages.success(request, f"You are now following {profile_user.name}.")
        return redirect('social_community:public_profile', user_id=user_id)

    return render(request, 'social_community/public_profile.html', {
        'profile_user': profile_user,
        'followed_count': followed_count,
        'followers_count': followers_count,
        'is_following': is_following,
        'current_user': current_user,
        'posts': posts_page,  # Pass paginated posts
    })

def community_features(request):
    if not check_login(request):
        return redirect("user-login")
    
    user = User.objects.get(id=request.session['user_id'])
    posts = Post.objects.all().select_related('user')
    post_form = PostForm()

    # Handle post creation
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = user
            post.save()
            messages.success(request, "Your post has been shared!")
            return redirect('social_community:community_features')
        else:
            post_form = PostForm()

    # Pagination for posts
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, 'social_community/community_features.html', {
        'user': user,
        'posts': posts_page,  # Pass paginated posts
        'post_form': post_form,
    })