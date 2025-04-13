from django.db import models
from django.contrib.auth.models import User
from apps.maps.models import Location
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

def default_checkout_time():
    return timezone.now() + timezone.timedelta(days=1)

class HotelBooking(models.Model):
    AMENITY_CHOICES = [
        ('wifi', 'WiFi'),
        ('ac', 'Air Conditioning'),
        ('breakfast', 'Breakfast'),
        ('pool', 'Swimming Pool'),
        ('parking', 'Parking'),
        ('gym', 'Gym'),
        ('spa', 'Spa'),
        ('tv', 'Television'),
        ('minibar', 'Minibar'),
    ]
    

    hotel_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to="hotel_photos/", null=True, blank=True)
    hotel_address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    total_person = models.IntegerField(default=1)  # Default to 1 person
    arrive_time = models.DateTimeField(default=timezone.now)  # Default to current time
    checkout_time = models.DateTimeField(default=default_checkout_time)  # Default to 1 day after now``
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True    , blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    email = models.EmailField(default='placeholder@example.com')
    ROOM_TYPE_CHOICES = [
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Standard', 'Standard'),
    ]
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES)
    rooms_available = models.BooleanField(default=True, verbose_name="Rooms Available")
    notify_admin = models.BooleanField(default=False)
    status = models.CharField(
    max_length=50,
    choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Pending', 'Pending')],
    default='Pending'  # Default value
)





    # ✅ New field for amenities
    amenity = models.CharField(max_length=100, choices=AMENITY_CHOICES, default='wifi')

    def __str__(self):
        return f"Hotel Booking at {self.hotel_name} - {self.user.username}"

    def clean(self):
      if self.amount <= 0:
        raise ValidationError("Amount must be greater than 0.")

     
      if self.total_person <= 0:
        raise ValidationError("Total persons must be at least 1.")

class HotelRoom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Standard', 'Standard'),
    ]
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES)

    room_number = models.CharField(max_length=100)
    
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=50,
        choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Occupied', 'Occupied')],
        default='Available'
    )
    hotel = models.ForeignKey('HotelBooking', on_delete=models.CASCADE, related_name='rooms')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

    def clean(self):
        # Additional validation for price
        if self.price_per_night <= 0:
            raise ValidationError("Price per night must be greater than 0.")


# Model to track hotel amenities (WiFi, AC, Breakfast, etc.)
# models.py


    

# Room Availability model to track availability per date

class RoomAvailability(models.Model):
    
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='availabilities')
    available_date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Availability for Room {self.room.room_number} on {self.available_date}"

    def clean(self):
        # Ensure availability date is in the future
        if self.available_date < date.today():
            raise ValidationError("Availability date cannot be in the past.")

# Revenue model to track hotel revenue



class HotelRevenue(models.Model):
    hotel_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    
class HotelReport(models.Model):
    REPORT_CHOICES = [
        ('Revenue', 'Revenue'),
        ('Availability', 'Room Availability'),
    ]
    hotel_booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50, choices=REPORT_CHOICES)
    report_date = models.DateField(default=timezone.now)
    report_data = models.JSONField()

    def __str__(self):
        return f"Report: {self.get_report_type_display()} for {self.hotel_booking.hotel_name} on {self.report_date}"

    def clean(self):
        # Validate that report data is not empty
        if not self.report_data:
            raise ValidationError("Report data cannot be empty.")
        
        
        
