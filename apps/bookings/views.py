# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required

# @login_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

# @login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})

# @login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form, 'booking': booking})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
