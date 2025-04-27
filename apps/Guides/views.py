from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import GuideForm
from .models import Guide
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login


# Custom test function to check if the user is an admin
def is_admin(user):
    return user.is_superuser or hasattr(user, 'loginadmin')


# List all guides with search and role context
def guide_list(request):
    query = request.GET.get('search', '')
    if query:
        guides = Guide.objects.filter(name__icontains=query)
    else:
        guides = Guide.objects.all()

    # Determine user role
    user_role = "User"
    if request.user.is_authenticated:
        if request.user.is_superuser or hasattr(request.user, 'loginadmin'):
            user_role = "Admin"

    return render(request, 'guides/guide_list.html', {
        'guides': guides,
        'user_role': user_role
    })


# View a single guide by primary key
def guide_view(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    return render(request, 'guides/guide_view.html', {'guide': guide})


# Detail view for to update/edit or delete a guide   
# This view is not accessible to regular users
@login_required 
def guide_edit_delete(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    return render(request, 'guides/guide_detail.html', {'guide': guide})


# Create a new guide — login required
@login_required
@user_passes_test(is_admin)
def guide_create(request):
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            

            guide = form.save(commit=False)
            
            guide.is_approved = False  # Set to False by default

            guide.save()
            form.save_m2m()
            return redirect('guide_list')
        else:
            return render(request, 'guides/guide_form.html', {'form': form})
    else:
        form = GuideForm()
    return render(request, 'guides/guide_form.html', {'form': form})


# Update an existing guide — login required
@login_required
@user_passes_test(is_admin)
def guide_update(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    form = GuideForm(request.POST or None, request.FILES or None, instance=guide)
    if request.method == 'POST':
        if form.is_valid():
            updated_guide = form.save(commit=False)
            updated_guide.save()
            form.save_m2m()
            return redirect('guide_list')
        else:
            return render(request, 'guides/guide_form.html', {'form': form, 'guide': guide})
    return render(request, 'guides/guide_form.html', {'form': form, 'guide': guide})


# Delete a guide — login required
@login_required
@user_passes_test(is_admin)
def guide_delete(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == 'POST':
        guide.delete()
        return redirect('guide_list')
    return render(request, 'guides/guide_confirm_delete.html', {'guide': guide})


# -------------------- USER VIEWS (Admin Only) --------------------

@login_required
@user_passes_test(is_admin)
def user_create(request):
    form = UserBaseCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, 'users/user_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = UserBase.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


# -------------------- OPTIONAL: Custom Login View --------------------

def custom_login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('guide_list')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')
