

# Django imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Count, Sum
from django.db import connection
from django.views.generic import ListView

# Third-party imports
from axes.helpers import get_lockout_response

# Local app imports
from .models import User, Wishlist, Trip, Notification
from .forms import WishlistForm, TripForm, ProfileUpdateForm, NotificationForm, UserForm, SignupForm, LoginForm, UserLoginForm

from apps.bookings.models import Booking
from apps.Guides.models import Guide
from apps.reviews.models import Review
from apps.Payments.models import Payment
from apps.tour_package.models import TourPackage
from apps.tourism_company.models import TourismCompany
from apps.social_community.models import Follow, Post
from apps.social_community.forms import FollowUserForm

# Standard library imports
import logging

# for user login to check supsicious login attempts
logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ------------------ AUTHENTICATION VIEWS ------------------

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_role'] = "Admin"  # Normal user role
                return redirect('user_login:admin-dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, "Invalid credentials, please try again.")
    else:
        form = LoginForm()
    return render(request, 'user_login/login.html', {'form': form})

# Logout View
@login_required
def admin_logout_view(request):
    request.session.flush()  # Logs out both session and Django user
    return redirect('user_login:login')  # Redirect to login page

# ------------------- USER VIEWS -------------------

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_login/create_user.html', {'form': form})

def view_user(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'user_login/view_user.html', {'user': user})

def user_list(request):
    query = request.GET.get('search', '')  # Get search query if exists
    if query:
        users = User.objects.filter(name__icontains=query)  # Filter users
    else:
        users = User.objects.all()  # Fetch all users
    return render(request, 'user_login/user_list.html', {'users': users, 'query': query})

def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            messages.error(request, "Error updating user.")
    else:
        form = UserForm(instance=user)
    return render(request, 'user_login/update_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':  
        user.delete()
        return redirect('user_list')
    return render(request, 'user_login/delete_user.html', {'user': user})

# ------------------ ADMIN DASHBOARD VIEW ------------------

@login_required(login_url='login')
def dashboard_view(request):
    users = User.objects.all()
    context = {
        'total_users': users.count(),
        'total_bookings': Booking.objects.count(),
        'total_guides': Guide.objects.count(),
        'total_reviews': Review.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_tour_packages': TourPackage.objects.count(),
        'total_tourism_companies': TourismCompany.objects.count(),
        'users': users,
    }
    return render(request, 'user_login/dashboard.html', context)

# ------------------- SIGNUP VIEWS -------------------

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Use secure hash
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('user-login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, 'user_login/user_signup.html', {'form': form})

# ------------------- USER LOGIN/LOGOUT -------------------

def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            ip = get_client_ip(request)

            try:
                user = User.objects.get(email=email)
                if check_password(password, user.password):  # Verify hashed password
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_role'] = "User"
                    request.session['is_Guest'] = False
                    request.session['is_superuser'] = False
                    return redirect('user_login:user_dashboard')
                else:
                    logger.warning(f"[{now()}] Invalid password attempt for {email} from IP {ip}")
                    messages.error(request, 'Invalid password')
            except User.DoesNotExist:
                logger.warning(f"[{now()}] Login attempt for non-existent user {email} from IP {ip}")
                messages.error(request, 'User not found')
    else:
        form = UserLoginForm()
    
    return render(request, 'user_login/user_login.html', {'form': form})


# FOR TOO MANY LOGIN ATTEMPTS 

def account_locked_view(request):
    return render(request, 'user_login/account_locked.html')

def user_logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_role' in request.session:
        del request.session['user_role']
    request.session.modified = True
    return redirect('user_login:user-login')

# ------------------- USER DASHBOARD VIEW -------------------

def user_dashboard_view(request):
    if "user_id" not in request.session:
        return redirect("user-login")
    
    user = User.objects.get(id=request.session["user_id"])
    wishlist = Wishlist.objects.filter(user=user)
    trips = Trip.objects.filter(user=user)
    notifications = Notification.objects.filter(user=user, is_read=False)
    
    wishlist_form = WishlistForm()
    trip_form = TripForm()
    profile_form = ProfileUpdateForm(instance=user)
    
    context = {
        "user": user,
        "wishlist": wishlist,
        "trips": trips,
        "notifications": notifications,
        "wishlist_form": wishlist_form,
        "trip_form": trip_form,
        "profile_form": profile_form,
    }
    return render(request, "user_login/user_dashboard.html", context)

# ------------------- ADD TO WISHLIST -------------------

def add_to_wishlist(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    
    user = User.objects.get(id=request.session["user_id"])
    if request.method == "POST":
        form = WishlistForm(request.POST)
        if form.is_valid():
            wishlist_item = form.save(commit=False)
            wishlist_item.user = user
            wishlist_item.save()
            messages.success(request, "Destination added to wishlist!")
            return redirect("user_login:user_details")
        else:
            messages.error(request, "Error adding to wishlist.")
    else:
        form = WishlistForm()
    
    return render(request, "user_login/add_to_wishlist.html", {"form": form})

# ------------------- ADD A TRIP -------------------

def add_trip(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")

    user = User.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = user
            trip.save()
            messages.success(request, "Trip added successfully!")
            return redirect("user_login:user_details")
        else:
            messages.error(request, "Error adding trip.")

    form = TripForm()
    return render(request, "user_login/add_trip.html", {"form": form})

# ------------------- UPDATE PROFILE -------------------

def update_profile(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")

    user = User.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("user_login:user_details")
        else:
            messages.error(request, "Error updating profile.")

    form = ProfileUpdateForm(instance=user)
    return render(request, "user_login/update_profile.html", {"form": form})

# ------------------- USER DETAILS VIEW -------------------

def user_details_view(request):
    if "user_id" not in request.session:
        return redirect("user-login")

    user = User.objects.get(id=request.session["user_id"])
    wishlist_items = Wishlist.objects.filter(user=user)
    trips = Trip.objects.filter(user=user)

    followed_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(followed=user).count()

    search_query = request.GET.get('search', '')
    if search_query:
        search_results = User.objects.filter(name__icontains=search_query).exclude(id=user.id)
    else:
        search_results = []

    if request.method == 'POST' and 'follow_user' in request.POST:
        user_to_follow_id = request.POST.get('user_to_follow')
        try:
            user_to_follow = User.objects.get(id=user_to_follow_id)
            if user_to_follow == user:
                messages.error(request, "You cannot follow yourself!")
            else:
                if Follow.objects.filter(follower=user, followed=user_to_follow).exists():
                    Follow.objects.filter(follower=user, followed=user_to_follow).delete()
                    messages.success(request, f"You have unfollowed {user_to_follow.name}.")
                else:
                    Follow.objects.create(follower=user, followed=user_to_follow)
                    messages.success(request, f"You are now following {user_to_follow.name}.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
        return redirect('user_details')
    
    return render(request, "user_login/user_details.html", {
        "user": user,
        "wishlist_items": wishlist_items,
        "trips": trips,
        "followed_count": followed_count,
        "followers_count": followers_count,
        "search_query": search_query,
        "search_results": search_results,
    })


