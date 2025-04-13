from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from apps.bookings.models import Booking
from .models import TourPackage
from apps.user_login.models import BookingDetail
from .forms import TourPackageForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.contrib.auth.models import User 
from apps.tourism_company.models import TourismCompany  
from apps.user_login.models import BookingDetail, User



# Total Tour package list 
def tour_package_list(request):
    user_role = request.session.get('user_role')

    if user_role == "Admin":
        packages = TourPackage.objects.all()  # Admin sees all packages
        # Admin can modify the (delete and edit package)
    elif user_role == "TourCompany":
         # Get company name from session
        packages = TourPackage.objects.filter(company_name=request.session.get('company_name'))  # Only their packages
    else:
        packages = TourPackage.objects.filter(is_approved=True)  # Regular users see only approved ones

    return render(request, 'tour_packages/package_list.html', {
        'packages': packages, 
        'user_role': user_role,
        'today': now().date()  # Send today's date to template for past date disabling
    })


from apps.tourism_company.models import TourismCompany  # import if needed

def add_tour_package(request):
    user_role = request.session.get('user_role')  # e.g., 'admin' or 'company'

    if request.method == "POST":
        form = TourPackageForm(request.POST, user_role=user_role)
        if form.is_valid():
            package = form.save(commit=False)
            package.is_approved = False  # Always False by default

            # Assign company only if user is a tourism company
            if user_role == 'company':
                company_id = request.session.get('company_id')
                if company_id:
                    package.tourism_company_id = company_id
                else:
                        # fallback if something's wrong
                    return HttpResponse("No company ID in session", status=400)
        else:
            return HttpResponse("Only companies can add packages", status=403)

        package.save()
        return redirect('tour_package:tour_package_list')
    else:
        form = TourPackageForm(user_role=user_role)

    return render(request, 'tour_packages/add_package.html', {'form': form})



#---------------------------------------------------------
# This view is for to book tour by user 

def book_tour(request, package_id):
    if request.session.get("user_role") != "User":
        return redirect("dashboard")  # Only users can book
    
    package = TourPackage.objects.get(package_id=package_id)
    
    if request.method == "POST":
        user_id = request.session.get("user_id")

#------------------------------
        if not user_id:
            print("Error: User ID not found in session!")
            return redirect("login")  # Redirect to login if session expired

            # Validate user_id
        try:
            user_id = int(user_id)  # Ensure user_id is an integer
        except (ValueError, TypeError):
            print(f"Error: Invalid user ID in session: {user_id}")
            request.session.flush()
            return redirect("login")
        
        # Ensure user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print(f"Error: User with ID {user_id} does not exist!")
            request.session.flush()
            return redirect("login")
          # ✅ Fix: Ensure user exists
        
        
        BookingDetail.objects.create(user=user, package=package)
#-----------------------------------------------
       # Booking.objects.create(user_id=user_id, package=package)
        return redirect("user_bookings")  # Redirect to user bookings page
    
    return render(request, 'tour_packages/book_tour.html', {"package": package})



# def book_tour(request, package_id):
#     if request.session.get("user_role") != "User":
#         return redirect("dashboard")  # Only users can book
    
#     package = TourPackage.objects.get(package_id=package_id)
    
#     if request.method == "POST":

 
#         user_id = request.session.get("user_id")

#         # ✅ Check if user_id exists in session
#         if not user_id:
#             print("Error: User ID not found in session!")
#             return redirect("login")  # Redirect to login if session expired

#         # ✅ Fix: Ensure user exists
#         user = User.objects.get(id=user_id)
        
#         Booking.objects.create(user=user, package=package)  # ✅ Fix: Use user instance
#         return redirect("user_bookings")  # Redirect to user bookings page
    
#     return render(request, 'tour_packages/book_tour.html', {"package": package})


#-----------------------------------------------------------------
#review package 

def review_package(request, package_id):
    if request.session.get('user_role') != "Admin":
        return redirect('tour_package_list')  # Redirect non-admins
    
    package = get_object_or_404(TourPackage, package_id=package_id)

    if request.method == "POST":
        package.is_approved = True  # Approve the package
        package.save()
        return redirect('tour_package_list')  # Redirect to list after approval

    return render(request, 'tour_packages/review_package.html', {'package': package})

#---------------------------------------------------------


# This is for admin to approve package after company add packages
@staff_member_required  # Only accessible by admin
def approve_tour_package(request, package_id):
    package = get_object_or_404(TourPackage, package_id=package_id)
    package.is_approved = True  # Mark as approved
    package.save()
    return redirect('admin_tour_package_list')  # Redirect back to the list

# View to edit a tour package
def edit_tour_package(request, package_id):
    package = TourPackage.objects.get(package_id=package_id)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            return redirect('tour_package:tour_package_list')
    else:
        form = TourPackageForm(instance=package)
    return render(request, 'tour_packages/edit_package.html', {'form': form, 'package': package})

# View to delete a tour package
def delete_tour_package(request, package_id):
    package = TourPackage.objects.get(package_id=package_id)
    if request.method == 'POST':
        package.delete()
        return redirect('tour_package_list')
    return render(request, 'tour_packages/delete_package.html', {'package': package})
