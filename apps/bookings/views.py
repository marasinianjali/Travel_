from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


# Custom test function to check if the user is an admin



def booking_list(request):
    
    bookings = Booking.objects.all()[:10]
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


from django.contrib.auth import get_user_model
User = get_user_model()
def create_booking(request):

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Booking created successfully!")
            return redirect('booking:booking_list')
        else:
            messages.error(request, "Please correct the errors below.")
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
            messages.success(request, "Booking updated successfully!")
            return redirect('booking:booking_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form, 'booking': booking})



def delete_booking(request, booking_id):
    if "user_id" not in request.session:
        return redirect("user_login:user-login")
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully!")
        return redirect('booking:booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})