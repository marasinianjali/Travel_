from django.shortcuts import render, redirect, get_object_or_404
from .models import HotelBooking
from .models import HotelBooking, HotelRoom
from .forms import HotelBookingForm
from .forms import HotelRoomForm, HotelBookingForm,HotelRevenue,HotelRevenueFilterForm
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.db.models import Q, Sum

#-----------------------------------------------------------

def view_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    return render(request, 'hotel_booking/view_hotel_room.html', {'room': room})


# Hotel Revenue List
def hotel_revenue_list(request):
    query = request.GET.get('q', '')  # Get search query from the request
    revenues = HotelRevenue.objects.all()

    if query:
        revenues = revenues.filter(Q(hotel_name__icontains=query) | Q(status__icontains=query))  # Search in name and status

    total_revenue = revenues.aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0
    



# List all hotel rooms
def hotel_rooms_list(request):
    rooms = HotelRoom.objects.all()  # Fetch all rooms
    room_count = rooms.count()  # Count total rooms
    return render(request, 'hotel_booking/hotel_rooms.html', {'rooms': rooms, 'room_count': room_count})



def add_hotel_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        status = request.POST.get('status')
        price_per_night = request.POST.get('price_per_night')
        description = request.POST.get('description')

        # Save new room
        room = HotelRoom(
            room_number=room_number,
            room_type=room_type,
            status=status,
            price_per_night=price_per_night,
            description=description
        )
        room.save()

        return redirect('hotel_rooms_list')

    return render(request, 'hotel_booking/add_hotel_room.html')



# Edit an existing hotel room
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

# Delete a hotel room
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

def hotel_dashboard(request):
    # Get the search query from the GET request (if any)
    search_query = request.GET.get('q', '')

    # Filter the bookings based on the search query, if provided
    if search_query:
        bookings = HotelBooking.objects.filter(hotel_name__icontains=search_query)
    else:
        bookings = HotelBooking.objects.all()

    # Calculate total bookings, revenue, and available rooms
    total_bookings = bookings.count()  # Use filtered bookings for total
    total_revenue = bookings.aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    # Get available rooms from the HotelRoom model
    available_rooms = HotelRoom.objects.filter(status='Available').count()

    # Prepare the context to be passed to the template
    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'available_rooms': available_rooms,
        'bookings': bookings,
    }

    return render(request, 'hotel_booking/hotel_dashboard.html', context)
def view_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    return render(request, 'hotel_booking/view_hotel_revenue.html', {'revenue': revenue})

def edit_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    
    if request.method == 'POST':
        form = HotelRevenueFilterForm(request.POST, instance=revenue)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking/hotel_revenue_list')  # Fixed redirect
    else:
        form = HotelRevenueFilterForm(instance=revenue)

    return render(request, 'hotel_booking/edit_hotel_revenue.html', {'form': form, 'revenue': revenue})

def delete_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    revenue.delete()
    return redirect('hotel_booking/hotel_revenue_list')  # Fixed redirect


# Approve or Reject a Booking
def change_booking_status(request, hotel_id, status):
    booking = get_object_or_404(HotelBooking, hotel_id=hotel_id)
    booking.status = status
    booking.save()
    return redirect('hotel_booking_list')










#------------------------------------------------------------
# List all hotel bookings
def hotel_booking_list(request):
    bookings = HotelBooking.objects.all()
    return render(request, 'hotel_booking/hotel_booking_list.html', {'bookings': bookings})

# Add a new hotel booking
def add_hotel_booking(request):
    if request.method == "POST":
        form = HotelBookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking_list')  # Redirect to the list page
    else:
        form = HotelBookingForm()
    return render(request, 'hotel_booking/add_hotel_booking.html', {'form': form})

# Edit a hotel booking
def edit_hotel_booking(request, hotel_id):
    booking = HotelBooking.objects.get(hotel_id=hotel_id)
    if request.method == "POST":
        form = HotelBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking_list')
    else:
        form = HotelBookingForm(instance=booking)
    return render(request, 'hotel_booking/edit_hotel_booking.html', {'form': form})

# Delete a hotel booking
def delete_hotel_booking(request, hotel_id):
    booking = HotelBooking.objects.get(hotel_id=hotel_id)
    booking.delete()
    return redirect('hotel_booking/hotel_booking_list')

