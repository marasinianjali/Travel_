# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test


def booking_list(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    
    bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


def create_booking(request):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})


def edit_booking(request, booking_id):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form, 'booking': booking})


def delete_booking(request, booking_id):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
