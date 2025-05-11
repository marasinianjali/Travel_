from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User

from apps.bookings.models import Booking
from apps.tour_package.models import TourPackage
from .models import TourismCompany
from .forms import TourismCompanyForm, CompanySignupForm, CompanyLoginForm, TourismCompanyCreateForm


# Custom role check
def is_tour_company(user):
    return user.is_authenticated and user.session.get("user_role") == "TourismCompany"


# ------------------- Company Signup -------------------

def company_signup(request):
    if request.method == "POST":
        form = CompanySignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('tourism_company:company_login')
    else:
        form = CompanySignupForm()
    return render(request, 'tourism_company/company_signup.html', {'form': form})


# ------------------- Company Login -------------------

def company_login(request):
    if request.method == "POST":
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']  # ← this is correct
            try:
                company = TourismCompany.objects.get(company_name=company_name)
                request.session['company_id'] = company.company_id
                request.session['company_name'] = company.company_name
                request.session['user_role'] = 'TourismCompany'
                request.session.modified = True
                return redirect('tourism_company:company_dashboard')
            except TourismCompany.DoesNotExist:
                form.add_error(None, "Invalid company details")
    else:
        form = CompanyLoginForm()
    return render(request, 'tourism_company/company_login.html', {'form': form})


# ------------------- Company Logout -------------------

def company_logout(request):
    request.session.flush()
    return redirect('tourism_company:company_login')


# ------------------- Company Dashboard -------------------


def company_dashboard_view(request):
    if request.session.get('user_role') != 'TourismCompany':
        return HttpResponseForbidden("Unauthorized access")
    return render(request, 'tourism_company/company_dashboard.html', {
        'user_role': request.session.get('user_role', 'Guest')
    })


# ------------------- Company Bookings -------------------

@login_required
def company_bookings(request):
    if request.session.get("user_role") != "TourismCompany":
        return redirect("tourism_company:company_login")

    company_name = request.session.get("company_name")
    bookings = Booking.objects.filter(package__company__company_name=company_name)

    return render(request, "tourism_company/bookings.html", {"bookings": bookings})


# ------------------- Company List -------------------

@login_required
def tourism_company_list(request):
    companies = TourismCompany.objects.all()
    return render(request, 'tourism_company/tourism_company_list.html', {'companies': companies})


# ------------------- Company Create -------------------

@login_required
def tourism_company_create(request):
    if request.method == 'POST':
        form = TourismCompanyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tourism_company:tourism_company_list')
    else:
        form = TourismCompanyCreateForm()
    return render(request, 'tourism_company/tourism_company_form.html', {'form': form})


# ------------------- Company Update -------------------

@login_required
def tourism_company_update(request, pk):
    company = get_object_or_404(TourismCompany, pk=pk)
    form = TourismCompanyForm(request.POST or None, instance=company)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('tourism_company:tourism_company_list')
    return render(request, 'tourism_company/tourism_company_form.html', {'form': form})


# ------------------- Company Delete -------------------

@login_required
def tourism_company_delete(request, pk):
    company = get_object_or_404(TourismCompany, pk=pk)
    if request.method == 'POST':
        company.delete()
        return redirect('tourism_company:tourism_company_list')
    return render(request, 'tourism_company/tourism_company_confirm_delete.html', {'company': company})
