from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User as AuthUser  # Django's built-in User model
from .models import User, Wishlist, Trip, Notification
from .forms import WishlistForm, TripForm, ProfileUpdateForm, NotificationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db import connection  # To run raw SQL queries

# URLS FOR USER LOGIN AND SIGNUP
from .forms import UserForm, SignupForm, LoginForm, UserLoginForm

# Import models for dashboard stats
from bookings.models import Booking
from Guides.models import Guide
from reviews.models import Review
from Payments.models import Payment
from tour_package.models import TourPackage
from tourism_company.models import TourismCompany
from django.contrib.auth.hashers import check_password

from social_community.models import Follow
from social_community.forms import FollowUserForm

#EXPENSES VIEWS
from expense_tracker.models import Expense, ExpenseCategory, ExpenseReport
from django.db import connection  # To run raw SQL queries
from django.views.generic import ListView
from expense_tracker.models import ExpenseCategory

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
                 # Set the user role for normal user
                request.session['user_role'] = "Admin"  # Normal user role
                #print(f"✅ Admin's User role set to  {request.session['user_role']}")
                return redirect('admin-dashboard')  # Redirect to dashboard after login
            else:
                return HttpResponse("Invalid credentials, please try again.")
    else:
        form = LoginForm()
    return render(request, 'user_login/login.html', {'form': form})


# Logout View
@login_required
def admin_logout_view(request):
    # Clear custom user session data
    request.session.flush()  # Logs out both session and Django user
    return redirect('login')  # Redirect to login page


# ------------------ USER MANAGEMENT VIEWS ------------------

# Create User View
# @login_required
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


# @login_required
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        print("POST request received")
        form = UserForm(request.POST, instance=user)
        print("Form data:", request.POST)  # See what data is being sent
        if form.is_valid():
            print("Form is valid, saving...")
            form.save()
            return redirect('user_list')
        else:
            print("Form errors:", form.errors)  # See why validation fails
    else:
        form = UserForm(instance=user)
    return render(request, 'user_login/update_user.html', {'form': form, 'user': user})

    
# Delete User View
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
    total_expenses = Expense.objects.count()
    total_expense_categories = ExpenseCategory.objects.count()
    total_expense_reports = ExpenseReport.objects.count()

    users = User.objects.all()  # Fetch all users
    context = {
        'total_users': users.count(),
        'total_bookings': Booking.objects.count(),
        'total_guides': Guide.objects.count(),
        'total_reviews': Review.objects.count(),
        'total_payments': Payment.objects.count(),
        'total_tour_packages': TourPackage.objects.count(),
        'total_tourism_companies': TourismCompany.objects.count(),
        'users': users,  # Pass users list to template
        'total_expenses': total_expenses,
        'total_expense_categories': total_expense_categories,
        'total_expense_reports': total_expense_reports,
    }
    print("✅ @login_required is being applied!")  # Debugging
    return render(request, 'user_login/dashboard.html', context)



class ExpenseCategoryListView(ListView):
    model = ExpenseCategory
    template_name = 'expense_tracker/expense_category_list.html'
    context_object_name = 'expense_categories'
    
from expense_tracker.models import ExpenseReport

class ExpenseReportListView(ListView):
    model = ExpenseReport
    template_name = 'expense_tracker/expense_report_list.html'


#-------------------------For user dashboard


#--------------------------FOR USERS TO SIGNUP BEFORE LOGIN 



def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = form.cleaned_data['password']  # Already hashed in form
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('user-login')  # Redirect to login after signup
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    
    return render(request, 'user_login/user_signup.html', {'form': form})




#-------------------------------FOR USER TO LOGIN AND CHECK 
#-------------------------------IF THE USER IS LOGGED IN OR NOT 


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)

                if check_password(password, user.password):  # Verify hashed password
                    # Store user information in session
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name 
                    request.session['user_role'] = "User"  # Normal user role


                    request.session['is_Guest'] = False    # 
                    request.session['is_superuser'] = False  # Custom users are not superusers
                    return redirect('user_dashboard')
                else:
                    messages.error(request, 'Invalid password')

            except User.DoesNotExist:
                messages.error(request, 'User not found')

    else:
        form = UserLoginForm()

    return render(request, 'user_login/user_login.html', {'form': form})




# def user_logout_view(request):
# 
def user_logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_role' in request.session:
        del request.session['user_role']
    request.session.modified = True
    return redirect('user-login')





    

# In user_dashboard_view
# views.py


from social_community.models import Post
# User Dashboard View
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


# Add to Wishlist (Updated to handle GET and POST)
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
            return redirect("user_details")
        else:
            messages.error(request, "Error adding to wishlist.")
    else:
        form = WishlistForm()
    
    return render(request, "user_login/add_to_wishlist.html", {"form": form})



# Add a Trip (Updated to handle GET and POST)

def add_trip(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")

    user = User.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = user  # ✅ Assign user before saving
            trip.save()
            messages.success(request, "Trip added successfully!")
            return redirect("user_details")  # ✅ Redirect to trip list
        else:
            messages.error(request, "Error adding trip.")

    form = TripForm()
    return render(request, "user_login/add_trip.html", {"form": form})



# Update Profile (Updated to handle GET and POST)
def update_profile(request):
    if "user_id" not in request.session:
        return redirect("user_login/user-login")  # Redirect to login if not logged in

    user = User.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("user_details")  
        else:
            messages.error(request, "Error updating profile.")

    form = ProfileUpdateForm(instance=user)
    return render(request, "user_login/update_profile.html", {"form": form})  



# Optional: Create Notification (for testing)
def create_notification(request):
    if request.method == "POST" and "user_id" in request.session:
        user = User.objects.get(user_id=request.session["user_id"])
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = user
            notification.save()
            messages.success(request, "Notification created!")
    return redirect("user_dashboard")





#---------------User details view 
#-------to show user their details when they click my account from user dashboard


def user_details_view(request):
    if "user_id" not in request.session:
        return redirect("user-login")  # Redirect if not logged in

    
    user = User.objects.get(id=request.session["user_id"])  # Fetch logged-in user
    wishlist_items = Wishlist.objects.filter(user=user)  #  Get wishlist items for the logged-in user
    trips = Trip.objects.filter(user=user)

    # Get total followers and following counts
    followed_count = Follow.objects.filter(follower=user).count() # Users the current user is following
    followers_count = Follow.objects.filter(followed=user).count() # Users following the current user

    # Search for other travelers
    search_query = request.GET.get('search', '')
    if search_query:
        # Exclude the current user from search results
        search_results = User.objects.filter(name__icontains=search_query).exclude(id=user.id)
    else:
        search_results = []

    # Handle follow/unfollow action
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


#----------------------------------------------------------------
# This view is for Users to Book their packages 


def user_bookings(request):
    if request.session.get("user_role") != "User":
        return redirect("user_dashboard")  # Only users can see their bookings

    user_id = request.session.get("user_id")
    user = request.user  
    if not user_id:
        print("User ID is missing from session!")
        return redirect("login")

    print("Fetching bookings for User ID:", user_id)
    
    bookings = Booking.objects.filter(user_name=user.username)


    #bookings = Booking.objects.filter(user=user_id)  # Changed 'user_id' to 'user'
    print("Bookings Found:", bookings)

    return render(request, "user_login/users_bookings.html", {"bookings": bookings})

#-----------------------------------------------------

