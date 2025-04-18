from django.db import models
from django.contrib.auth.models import User
from apps.hotelbooking.models import HotelBooking
from apps.tour_package.models import TourPackage
from apps.Guides.models import Guide

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ]

    booking_id = models.AutoField(
        primary_key=True,
        verbose_name="Booking ID",
        help_text="Unique identifier for the booking."
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="User who made the booking."
    )
    hotel = models.ForeignKey(
        HotelBooking,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Hotel",
        help_text="Associated hotel booking, if any."
    )
    user_name = models.CharField(
        max_length=255,
        verbose_name="User Name",
        help_text="Name of the user who booked the package."
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Phone Number",
        help_text="Phone number of the user."
    )
    total_members = models.IntegerField(
        verbose_name="Total Members",
        help_text="Number of people included in the booking."
    )
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        verbose_name="Tour Package",
        help_text="Tour package selected by the user."
    )
    guide = models.ForeignKey(
        Guide,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Guide",
        help_text="Tour guide assigned to the booking, if any."
    )
    booking_date = models.DateField(
        verbose_name="Booking Date",
        help_text="Date when the booking was made."
    )
    booking_details = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Booking Details",
        help_text="Additional details or notes about the booking."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        verbose_name="Status",
        help_text="Current status of the booking."
    )
    promecode = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Promo Code",
        help_text="Applied promo code for discount, if any."
    )
    pickup_location = models.CharField(
        max_length=255,
        verbose_name="Pickup Location",
        help_text="Location where the customer will be picked up."
    )

    def __str__(self):
        return f"Booking #{self.booking_id} - {self.user.username if self.user else 'No User'}"

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        db_table = "Bookings"
