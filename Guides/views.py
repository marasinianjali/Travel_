from django.shortcuts import render, redirect, get_object_or_404
from .forms import GuideForm
from .models import Guide

#View for listing all guides
# def guide_list(request):
#     guides = Guide.objects.all()
#     return render(request, 'guides/guide_list.html', {'guides': guides})

def guide_list(request):
    guides = Guide.objects.all()

    # Default role is User
    user_role = "User"

    # Check if the user is authenticated and part of Django's admin system
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_role = "Admin"
        elif hasattr(request.user, 'loginadmin'):  # Check if the user is part of your `LoginAdmin` model
            user_role = "Admin"
    query = request.GET.get('search', '')  # Get the search query from the GET request
    if query:
        # Filter guides by name if the search query exists
        guides = Guide.objects.filter(name__icontains=query)
    else:
        guides = Guide.objects.all()  # Show all guides if no search query is provided
    

    return render(request, 'guides/guide_list.html', {
        'guides': guides,
        'user_role': user_role,  # Pass role to the template
    })

def guide_view(request, guide_id):
    guide = get_object_or_404(Guide, guide_id=guide_id)  # Use 'guide_id' instead of 'id'
    return render(request, 'guides/guide_view.html', {'guide': guide})

def guide_create(request):
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guide_list')  # Redirect to the guide list page after creating
    else:
        form = GuideForm()
    return render(request, 'guides/guide_form.html', {'form': form})

def guide_detail(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    return render(request, 'guides/guide_detail.html', {'guide': guide})

def guide_update(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    
    if request.method == 'POST':
        form = GuideForm(request.POST, request.FILES, instance=guide)
        if form.is_valid():
            form.save()
            return redirect('guide_list')
    else:
        form = GuideForm(instance=guide)

    return render(request, 'guides/guide_form.html', {'form': form, 'guide': guide})

# Delete guide
def guide_delete(request, guide_id):  # `guide_id` here matches the URL parameter
    guide = get_object_or_404(Guide, pk=guide_id)
    if request.method == 'POST':
        guide.delete()
        return redirect('guide_list')  # Redirect back to the guide list after deletion
    return render(request, 'guides/guide_confirm_delete.html', {'guide': guide})
