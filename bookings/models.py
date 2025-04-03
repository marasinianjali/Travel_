from django.db import models
from django.contrib.auth.models import User  # Assuming Users refers to Django's User model
from hotelbooking.models import HotelBooking
from tour_package.models import TourPackage
from Guides.models import Guide

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]

    booking_id = models.AutoField(primary_key=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    total_members = models.IntegerField()
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)
    booking_date = models.DateField()
    booking_details = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    promecode = models.CharField(max_length=50, blank=True, null=True)
    pickup_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Booking #{self.booking_id} - {self.user.username}"
    
    # Telling django use this table 
    class Meta:
        db_table = 'Bookings'
