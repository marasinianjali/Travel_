
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LocationForm
from .models import Location

#-----------------------------------------------------
# Views for managing Locations
#-----------------------------------------------------

# Add a new location
def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to the location list page
    else:
        form = LocationForm()
    return render(request, 'maps/add_location.html', {'form': form})

# List all locations
def location_list(request):
    locations = Location.objects.all()  # Fetch all locations from the database
    return render(request, 'maps/location_list.html', {'locations': locations})

# View the details of a single location
def location_detail(request, id):
    location = get_object_or_404(Location, id=id)
    return render(request, 'maps/location_detail.html', {'location': location})



