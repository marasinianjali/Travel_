from django.db import models
from fernet_fields import EncryptedCharField


from django.contrib.auth.models import User
from apps.maps.models import Location
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone
from datetime import date
from fernet_fields import EncryptedCharField,  EncryptedEmailField

from fernet_fields import EncryptedField
from django.db import models
from decimal import Decimal

class EncryptedDecimalField(EncryptedField, models.TextField):
    def get_prep_value(self, value):
        if value is None:
            return value
        return str(Decimal(value))  # Convert to string for encryption

    def to_python(self, value):
        if value is None:
            return value
        try:
            return Decimal(value)
        except:
            return Decimal('0.00')

# Language model for normalization
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Language Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"


# Default checkout time function
def default_checkout_time():
    return timezone.now() + timezone.timedelta(days=1)


# Abstract base for guides
class GuideBase(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Full Name", help_text="Enter the full name of the guide.")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    profile_picture = models.ImageField(upload_to='guide_profiles/', blank=True, null=True, verbose_name="Profile Picture")
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], verbose_name="Rating")
    experience_years = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)], verbose_name="Years of Experience")
    languages = models.ManyToManyField(Language, verbose_name="Languages Spoken")

    class Meta:
        abstract = True
        verbose_name = "Guide Base"
        verbose_name_plural = "Guide Bases"

    def clean(self):
        if not (0 <= self.experience_years <= 50):
            raise ValidationError("Experience must be between 0 and 50 years.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Guide(GuideBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guide_profile', verbose_name="User")

    def __str__(self):
        return f"{self.name} (Guide)"

    class Meta:
        verbose_name = "Guide"
        verbose_name_plural = "Guides"


class HotelBooking(models.Model):
    AMENITY_CHOICES = [
        ('wifi', 'WiFi'), ('ac', 'Air Conditioning'), ('breakfast', 'Breakfast'),
        ('pool', 'Swimming Pool'), ('parking', 'Parking'), ('gym', 'Gym'),
        ('spa', 'Spa'), ('tv', 'Television'), ('minibar', 'Minibar'),
    ]
    ROOM_TYPE_CHOICES = [('Deluxe', 'Deluxe'), ('Suite', 'Suite'), ('Standard', 'Standard')]
    STATUS_CHOICES = [('Available', 'Available'), ('Booked', 'Booked'), ('Pending', 'Pending')]

    hotel_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    hotel_name = models.CharField(max_length=255, 
                                  verbose_name="Hotel Name")
    amount = EncryptedDecimalField(default=1000.00, 
                                   validators=[MinValueValidator(0.01)], 
                                   verbose_name="Base Amount")
    photo = models.ImageField(upload_to="hotel_photos/", null=True, blank=True, verbose_name="Hotel Photo")
    hotel_address = models.CharField(max_length=255, verbose_name="Hotel Address")
    contact_number = EncryptedCharField(max_length=20, verbose_name="Contact Number")
    total_person = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Total Persons")
    arrive_time = models.DateTimeField(verbose_name="Arrival Time")
    checkout_time = models.DateTimeField(default=default_checkout_time, verbose_name="Checkout Time")
    total_price = EncryptedDecimalField(default=1000.00,  
                                        verbose_name="Total Price")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, verbose_name="Location")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, 
                                    decimal_places=6, null=True, blank=True, verbose_name="Longitude")
                                    
    email = EncryptedEmailField(max_length=254, verbose_name="Email Address")

    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES, verbose_name="Room Type")
    rooms_available = models.BooleanField(default=True, verbose_name="Rooms Available")
    notify_admin = models.BooleanField(default=False, verbose_name="Notify Admin")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', verbose_name="Booking Status")
    amenity = models.CharField(max_length=100, choices=AMENITY_CHOICES, verbose_name="Amenity")

    def __str__(self):
        return f"{self.hotel_name} booking by {self.user.username}"

    def clean(self):
        if self.checkout_time <= self.arrive_time:
            raise ValidationError("Checkout time must be after arrival time.")

    class Meta:
        verbose_name = "Hotel Booking"
        verbose_name_plural = "Hotel Bookings"


class HotelRoom(models.Model):
    ROOM_TYPE_CHOICES = [('Deluxe', 'Deluxe'), ('Suite', 'Suite'), ('Standard', 'Standard')]
    STATUS_CHOICES = [('Available', 'Available'), ('Booked', 'Booked'), ('Occupied', 'Occupied')]

    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES, verbose_name="Room Type")
    room_number = models.CharField(max_length=100, verbose_name="Room Number")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Price per Night")
    description = models.TextField(verbose_name="Room Description")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Available', verbose_name="Room Status")
    hotel = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, related_name='rooms', verbose_name="Hotel")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude")

    def __str__(self):
        return f"Room {self.room_number} - {self.get_room_type_display()}"

    class Meta:
        verbose_name = "Hotel Room"
        verbose_name_plural = "Hotel Rooms"


class RoomAvailability(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='availabilities', verbose_name="Room")
    available_date = models.DateField(verbose_name="Available Date")
    is_available = models.BooleanField(default=True, verbose_name="Is Available")

    def __str__(self):
        return f"{self.room.room_number} on {self.available_date}: {'Available' if self.is_available else 'Not Available'}"

    def clean(self):
        if self.available_date < date.today():
            raise ValidationError("Available date cannot be in the past.")

    class Meta:
        verbose_name = "Room Availability"
        verbose_name_plural = "Room Availabilities"


class HotelRevenue(models.Model):
    hotel_name = models.CharField(max_length=255, verbose_name="Hotel Name")
    amount = EncryptedDecimalField(default=1000.00, 
                                    validators=[MinValueValidator(0.01)], 
                                    verbose_name="Amount")
    status = models.CharField(max_length=50, verbose_name="Payment Status")

    def __str__(self):
        return f"{self.hotel_name} - {self.amount} ({self.status})"

    class Meta:
        verbose_name = "Hotel Revenue"
        verbose_name_plural = "Hotel Revenues"


class HotelReport(models.Model):
    REPORT_CHOICES = [('Revenue', 'Revenue'), ('Availability', 'Room Availability')]

    hotel_booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, related_name='reports', verbose_name="Hotel Booking")
    report_type = models.CharField(max_length=50, choices=REPORT_CHOICES, verbose_name="Report Type")
    report_date = models.DateField(default=timezone.now, verbose_name="Report Date")
    report_data = models.JSONField(verbose_name="Report Data")

    def __str__(self):
        return f"{self.get_report_type_display()} Report for {self.hotel_booking.hotel_name} on {self.report_date}"

    def clean(self):
        if not self.report_data:
            raise ValidationError("Report data cannot be empty.")

    class Meta:
        verbose_name = "Hotel Report"
        verbose_name_plural = "Hotel Reports"
