from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import HotelBooking, HotelRoom, HotelRevenue, RoomAvailability, HotelReport
from .forms import HotelBookingForm, HotelRevenueFilterForm, RoomAvailabilityForm, LoginForm, HotelReportForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import RoomAvailability

#-----------------------------------------------------
# Helper Function for Role-based Access Control
def is_admin(user):
    return user.is_staff  # Modify this logic based on your requirements (e.g., checking group or custom permission)

#-----------------------------------------------------

# View for hotel rooms
def view_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    return render(request, 'hotel_booking/view_hotel_room.html', {'room': room})

# List all hotel rooms
def hotel_rooms_list(request):
    rooms = HotelRoom.objects.all()
    room_count = rooms.count()
    return render(request, 'hotel_booking/hotel_rooms.html', {'rooms': rooms, 'room_count': room_count})

# Add a new hotel room - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def add_hotel_room(request):
    if request.method == 'POST':

        hotel_id = request.POST.get('hotel_id')
        hotel = get_object_or_404(HotelBooking, id=hotel_id)
        
        if hotel.is_valid():
            room = hotel.save(commit=False)
            room.is_approved = False


        room = HotelRoom(
            hotel=hotel,
            room_number=request.POST.get('room_number'),
            room_type=request.POST.get('room_type'),
            status=request.POST.get('status'),
            price_per_night=request.POST.get('price_per_night'),
            description=request.POST.get('description')
        )
        room.save()
        return redirect('hotel_rooms_list')
    hotels = HotelBooking.objects.all()
    return render(request, 'hotel_booking/add_hotel_room.html', {'hotels': hotels})

# Edit an existing hotel room - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def edit_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    if request.method == 'POST':
        room.room_number = request.POST.get('room_number')
        room.room_type = request.POST.get('room_type')
        room.status = request.POST.get('status')
        room.price_per_night = request.POST.get('price_per_night')
        room.description = request.POST.get('description')
        room.save()
        return redirect('hotel_rooms_list')
    return render(request, 'hotel_booking/edit_hotel_room.html', {'room': room})

# Delete a hotel room - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def delete_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    room.delete()
    return redirect('hotel_rooms_list')

# List all hotel bookings with search & filter
def hotel_booking_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    bookings = HotelBooking.objects.all()
    if query:
        bookings = bookings.filter(hotel_name__icontains=query)
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'hotel_booking/hotel_booking_list.html', {'bookings': bookings})

# Hotel Login View
def hotel_login_view(request):
    if request.user.is_authenticated:
        return redirect('hotel_dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('hotel_dashboard')
            else:
                return render(request, 'hotel_booking/hotel_login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'hotel_booking/hotel_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('hotel_login')

# Hotel Dashboard
@login_required(login_url='hotel_login/')
def hotel_dashboard(request):
    total_bookings = HotelBooking.objects.count()
    total_revenue = sum(b.total_price for b in HotelBooking.objects.all())
    available_rooms = HotelRoom.objects.filter(status='Available')
    hotels = HotelBooking.objects.all()
    total_room_availability = RoomAvailability.objects.count()
    hotel_name = "Your Hotel Name"
    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'available_rooms': available_rooms,
        'hotels': hotels,
        'total_room_availability': total_room_availability,
        'hotel_name': hotel_name,
    }
    return render(request, 'hotel_booking/hotel_dashboard.html', context)

# Hotel Revenue Views
@login_required
@user_passes_test(is_admin)
def edit_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    if request.method == 'POST':
        form = HotelRevenueFilterForm(request.POST, instance=revenue)
        if form.is_valid():
            form.save()
            return redirect('hotel_revenue_list')
    else:
        form = HotelRevenueFilterForm(instance=revenue)
    return render(request, 'hotel_booking/edit_hotel_revenue.html', {'form': form, 'revenue': revenue})

# Delete Hotel Revenue - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def delete_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    revenue.delete()
    return redirect('hotel_revenue_list')

# Hotel Booking Views
@login_required
def add_hotel_booking(request):
    if request.method == "POST":
        form = HotelBookingForm(request.POST, request.FILES)
        if form.is_valid():
            hotel_booking = form.save(commit=False)
            hotel_booking.user = request.user
            hotel_booking.status = 'Pending'
            hotel_booking.save()
            return redirect('hotel_booking_list')
    else:
        form = HotelBookingForm()
    return render(request, 'hotel_booking/add_hotel_booking.html', {'form': form})

# Edit and Delete Hotel Booking - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def edit_hotel_booking(request, hotel_id):
    booking = get_object_or_404(HotelBooking, hotel_id=hotel_id)
    if request.method == "POST":
        form = HotelBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking_list')
    else:
        form = HotelBookingForm(instance=booking)
    return render(request, 'hotel_booking/edit_hotel_booking.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_hotel_booking(request, hotel_id):
    booking = get_object_or_404(HotelBooking, hotel_id=hotel_id)
    booking.delete()
    return redirect('hotel_booking_list')

# Add Room Availability - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def add_room_availability(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.room = room
            availability.save()
            return redirect('room-availability-list')
    else:
        form = RoomAvailabilityForm()
    return render(request, 'hotel_booking/add_room_availability.html', {'form': form, 'room': room})

# Edit and Delete Room Availability - Only accessible by admin
@login_required
@user_passes_test(is_admin)
def edit_availability(request, pk):
    availability = get_object_or_404(RoomAvailability, pk=pk)
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('hotel_dashboard')
    else:
        form = RoomAvailabilityForm(instance=availability)
    return render(request, 'hotel_booking/edit_room_availability.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_availability(request, pk):
    availability = get_object_or_404(RoomAvailability, pk=pk)
    availability.delete()
    return redirect('hotel_dashboard')




#------------------------------------------------------
def hotel_revenue_list(request):
    query = request.GET.get('q', '')  # Get search query from the request

    # Retrieve all HotelRevenue records, no filtering by user since user is not a field
    revenues = HotelRevenue.objects.all()

    # If a query is present, filter by hotel name or status
    if query:
        revenues = revenues.filter(
            Q(hotel_name__icontains=query) | Q(status__icontains=query)
        )

    # Calculate total revenue
    total_revenue = revenues.aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    # Enhance each object dynamically (peak season and average value if needed)
    
    # Ensure the render statement is always returned
    return render(request, 'hotel_booking/hotel_revenue_list.html', {
        'revenues': revenues,
        'total_revenue': total_revenue,
        'query': query,
    })

def view_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    return render(request, 'hotel_booking/view_hotel_revenue.html', {'revenue': revenue})


def room_availability_list(request):
    availability_list = RoomAvailability.objects.select_related('room__hotel').all()
    hotel_id = None

    if availability_list:
        first_availability = availability_list.first()
        if first_availability.room and first_availability.room.hotel:
            hotel_id = first_availability.room.hotel.hotel_id

    return render(request, 'hotel_booking/room_availability_list.html', {
        'availability_list': availability_list,
        'hotel_id': hotel_id,
    })


def view_room_availability(request, hotel_id):
    hotel = get_object_or_404(HotelBooking, pk=hotel_id)
    rooms = hotel.rooms.all()
    room_availabilities = RoomAvailability.objects.filter(room__in=rooms)
    return render(request, 'hotel_booking/view_room_availability.html', {
        'hotel': hotel,
        'room_availabilities': room_availabilities,
    })
def hotel_report_list(request):
    reports = HotelReport.objects.all()
    return render(request, 'hotel_booking/report_list.html', {'reports': reports})

# Create Report
def hotel_report_create(request):
    if request.method == 'POST':
        form = HotelReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel report created successfully.")
            return redirect('hotel_report_list')
    else:
        form = HotelReportForm()
    return render(request, 'hotel_booking/report_form.html', {'form': form, 'title': 'Create Hotel Report'})


# Update Report
def hotel_report_update(request, pk):
    report = get_object_or_404(HotelReport, pk=pk)
    if request.method == 'POST':
        form = HotelReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Hotel report updated successfully.")
            return redirect('hotel_report_list')
    else:
        form = HotelReportForm(instance=report)
    return render(request, 'hotel_booking/report_form.html', {'form': form, 'title': 'Update Hotel Report'})


# Delete Report
def hotel_report_delete(request, pk):
    report = get_object_or_404(HotelReport, pk=pk)
    if request.method == 'POST':
        report.delete()
        messages.success(request, "Hotel report deleted successfully.")
        return redirect('hotel_report_list')
    return render(request, 'hotel_booking/report_confirm_delete.html', {'report': report})
