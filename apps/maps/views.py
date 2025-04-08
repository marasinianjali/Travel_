from django.shortcuts import render, redirect
from .forms import LocationForm
from .models import Location
# maps/views.py
from django.shortcuts import render, get_object_or_404


def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('location_list')  # Redirect to location list page
    else:
        form = LocationForm()
    return render(request, 'maps/add_location.html', {'form': form})

def location_list(request):
    locations = Location.objects.all()  # Fetch all locations from the database
    return render(request, 'maps/location_list.html', {'locations': locations})
def location_detail(request, id):
    location = get_object_or_404(Location, id=id)
    return render(request, 'maps/location_detail.html', {'location': location})
