from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.timezone import now
from .forms import TourPackageForm
from .models import TourPackage
from apps.bookings.models import Booking
from apps.user_login.models import User


# Custom check for admin
# def is_admin(user):
#     return user.is_superuser or hasattr(user, 'loginadmin')


# List all tour packages
from django.utils.timezone import now
from .models import TourPackage

def tour_package_list(request):
    user_role = request.session.get('user_role')

    if user_role == "Admin":
        packages = TourPackage.objects.all()
    elif user_role == "TourCompany":
        company_id = request.session.get('company_id')  # Use company_id now
        packages = TourPackage.objects.filter(tourism_company_id=company_id)
    else:
        packages = TourPackage.objects.filter(is_approved=True)

    return render(request, 'tour_packages/package_list.html', {
        'packages': packages,
        'user_role': user_role,
        'today': now().date()
    })



# Add a new tour package

def add_tour_package(request):
    user_role = request.session.get('user_role')

    if request.method == "POST":
        form = TourPackageForm(request.POST, user_role=user_role)
        if form.is_valid():
            package = form.save(commit=False)
            package.is_approved = False

            if user_role == 'TourismCompany':
                company_id = request.session.get('company_id')
                if company_id:
                    package.tourism_company_id = company_id
                    package.save()
                    return redirect('tour_package:tour_package_list')
                else:
                    return HttpResponse("No company ID in session", status=400)
            else:
                return HttpResponse("Only tourism companies can add packages", status=403)
    else:
        form = TourPackageForm(user_role=user_role)

    return render(request, 'tour_packages/add_package.html', {'form': form})


# Edit a tour package
@login_required
def edit_tour_package(request, package_id):
    package = get_object_or_404(TourPackage, package_id=package_id)
    form = TourPackageForm(request.POST or None, instance=package)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('tour_package:tour_package_list')

    return render(request, 'tour_packages/edit_package.html', {
        'form': form,
        'package': package
    })


# Delete a tour package
@login_required
def delete_tour_package(request, package_id):
    package = get_object_or_404(TourPackage, package_id=package_id)

    if request.method == "POST":
        package.delete()
        return redirect('tour_package:tour_package_list')

    return render(request, 'tour_packages/delete_package.html', {'package': package})


# Admin review & approval page
@login_required

def review_package(request, package_id):
    package = get_object_or_404(TourPackage, package_id=package_id)

    if request.method == "POST":
        package.is_approved = True
        package.save()
        return redirect('tour_package:tour_package_list')

    return render(request, 'tour_packages/review_package.html', {'package': package})


# Admin approve directly (staff-only)
@login_required

def approve_tour_package(request, package_id):
    package = get_object_or_404(TourPackage, package_id=package_id)
    package.is_approved = True
    package.save()
    return redirect('admin_tour_package_list')


# Book tour view 
# @login_required
# def book_tour(request, package_id):
#     if request.session.get("user_role") != "User":
#         return redirect("dashboard")
#     package = get_object_or_404(TourPackage, package_id=package_id)
#     if request.method == "POST":
#         user_id = request.session.get("user_id")
#         if not user_id:
#             return redirect("login")
#         user = get_object_or_404(User, id=user_id)
#         Booking.objects.create(user=user, package=package)
#         return redirect("user_bookings")
#     return render(request, 'tour_packages/book_tour.html', {"package": package})
