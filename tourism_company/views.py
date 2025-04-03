from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import TourismCompany
from .forms import TourismCompanyForm, CompanySignupForm, CompanyLoginForm
from tour_package.models import TourPackage
from user_login.models import Booking
# from django.contrib.auth.models import User
from django.contrib.auth.models import User  





#-------------------------------------------------------------------
# This view is for company signup

def company_signup(request):
    if request.method == "POST":
        form = CompanySignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('company_login')
    else:
        form = CompanySignupForm()
    return render(request, 'tourism_company/company_signup.html', {'form': form})


#-------------------------------------------------------------------
# This view is for company login


def company_login(request):
    if request.method == "POST":
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            try:
                company = TourismCompany.objects.get(company_name=company_name)
                
                # Store session data
                request.session['company_id'] = company.company_id
                request.session["company_name"] = company.company_name 
                request.session['user_role'] = "TourismCompany"
                request.session.modified = True  # Force session save
                
               

                return redirect('company_dashboard')  

            except TourismCompany.DoesNotExist:
                form.add_error(None, "Invalid company details")

    else:
        form = CompanyLoginForm()

    return render(request, 'tourism_company/company_login.html', {'form': form})



#-------------------------------------------------------------------
# This view is for company logout

def company_logout(request):
    if 'company_id' in request.session:
        del request.session['company_id']
    if 'user_role' in request.session:
        del request.session['user_role']  # Remove only role instead of flushing
    request.session.modified = True  # Ensure changes are saved
    return redirect('tourism_company/company_login')



#-------------------------------------------------------------------
# This view is for company dashboard


def company_dashboard_view(request):
    # Check if the company is logged in
    if 'company_id' not in request.session:
        return redirect('company_login')  # Redirect to login if not logged in

    return render(request, 'tourism_company/company_dashboard.html', {
        'user_role': request.session.get('user_role', 'Guest')
    })
    
#-----------------------------------------------------------------------------------------
# This view is using for compnay to show their total booking of the package posted by them


def company_bookings(request):
    if request.session.get("user_role") != "TourismCompany":
        return redirect("dashboard")

    company_name = request.session.get("company_name")  # Assuming this is how you store it
    if not company_name:
        print("Company name is missing from session!")
        return redirect("dashboard")

    # Filter bookings where the package's company matches the session company_name
    bookings = Booking.objects.filter(package__company__name=company_name)

    
    # Debugging
    for booking in bookings:
        print(f"Booking ID: {booking.booking_id}, User Name: {booking.user.username}") # Updated to use 'user.username'
    print("Bookings:", bookings)

    return render(request, "tourism_company/bookings.html", {"bookings": bookings})

# def company_bookings(request):
#     if request.session.get("user_role") != "Company":
#         return redirect("dashboard")  # Only companies can see total bookings

#     company_name = request.session.get("company_name")

#     if not company_name:
#         print("Company name is missing from session!")
#         return redirect("dashboard")

#     # Fetch bookings for the given company
#     bookings = Booking.objects.filter(package__company_name=company_name).select_related("package")

#     # Create a list of bookings with user details attached
#     for booking in bookings:
#         try:
#             # Fetch the associated user for each booking
#             booking.user = User.objects.get(id=booking.user_id)
#         except User.DoesNotExist:
#             booking.user = None  # Handle the case where the user doesn't exist

#     return render(request, "tourism_company/company_bookings.html", {"bookings": bookings})


#----------------------------------------------------------------
#Total tourism company list 

def tourism_company_list(request):
    companies = TourismCompany.objects.all()
    return render(request, 'tourism_company/tourism_company_list.html', {'companies': companies})


def tourism_company_create(request):
    if request.method == 'POST':
        form = TourismCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tourism_company_list')  # Redirect to the list view after saving
    else:
        form = TourismCompanyForm()
    return render(request, 'tourism_company/tourism_company_form.html', {'form': form})



#----------------------------------------------------------------------------
def tourism_company_update(request, pk):
    company = get_object_or_404(TourismCompany, pk=pk)
    if request.method == 'POST':
        form = TourismCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('tourism_company_list')  # Redirect to the list view after updating
    else:
        form = TourismCompanyForm(instance=company)
    return render(request, 'tourism_company/tourism_company_form.html', {'form': form})

def tourism_company_update(request, package_id):
    # Check if the user has the correct role
    if request.session.get('user_role') not in ['Admin', 'TourismCompany']:
        return redirect('not_authorized')  # Redirect to a 'not authorized' page

    # Continue with the logic for editing the package
    package = TourPackage.objects.get(id=package_id)
    # Your editing logic goes here...

    return render(request, 'tourism_company/tourism_company_form.html', {'package': package})


#----------------------------------------------------------------------------------------------------------
# Delete view: Delete an existing company
def tourism_company_delete(request, pk):
    company = get_object_or_404(TourismCompany, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('tourism_company_list')  # Redirect to the list view after deleting
    return render(request, 'tourism_company/tourism_company_confirm_delete.html', {'company': company})

