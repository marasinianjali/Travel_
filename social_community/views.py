from django.shortcuts import render, redirect, get_object_or_404
from user_login.models import User
from .models import Follow, Post
from django.contrib import messages
from .forms import PostForm
from social_community.models import Category
Category.objects.all()  

def check_login(request):
    if "user_id" not in request.session:
        return False
    return True

def followed_list(request):
    if not check_login(request):
        return redirect("user-login")

    user = User.objects.get(id=request.session["user_id"])
    search_query = request.GET.get('search', '')
    followed = Follow.objects.filter(follower=user).select_related('followed')

    if search_query:
        followed = followed.filter(followed__name__icontains=search_query)
    
    return render(request, 'social_community/following_list.html', {
        'followed': followed,
        'search_query': search_query,
    })


def followers_list(request):
    if not check_login(request):
        return redirect("user-login")

    user = User.objects.get(id=request.session["user_id"])
    followers = Follow.objects.filter(followed=user).select_related('follower')
    return render(request, 'social_community/followers_list.html', {'followers': followers})


def community_features(request):
    if not check_login(request):
        return redirect("user-login")

    return render(request, 'social_community/community_features.html', {})


# User's Public Profile view 
def public_profile(request, user_id):
    if not check_login(request):
        return redirect("user-login")

    current_user = User.objects.get(id=request.session["user_id"])
    profile_user = get_object_or_404(User, id=user_id)

    # Get total followers and following counts for the profile user
    followed_count = Follow.objects.filter(follower=profile_user).count()
    followers_count = Follow.objects.filter(followed=profile_user).count()
    is_following = Follow.objects.filter(follower=current_user, followed=profile_user).exists()

    posts = Post.objects.filter(user=profile_user).select_related('user')

    # Handle follow/unfollow action
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
        'posts':posts,
    })



def community_features(request):
    if not check_login(request):
        return redirect("user-login")
    
    user = User.objects.get(id=request.session['user_id'])

    # Get all posts (or optionally, posts from followed users)
    posts = Post.objects.all().select_related('user')
     # Initialize post_form to avoid UnboundLocalError
    post_form = PostForm()  

    # Handle post creating
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

    return render(request, 'social_community/community_features.html',{
        'user':user,
        'posts': posts,
        'post_form': post_form,
    })

