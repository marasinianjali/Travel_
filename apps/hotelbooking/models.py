from django.db import models
from django.contrib.auth.models import User  # Assuming Users is linked to Django's User model

class HotelBooking(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to Users
    hotel_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Ensuring amount > 0 at form validation level
    room_type = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="hotel_photos/", null=True, blank=True)
    hotel_address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    total_person = models.IntegerField()
    arrive_time = models.DateTimeField()
    checkout_time = models.DateTimeField()

    def __str__(self):
        return f"Hotel Booking at {self.hotel_name} - {self.user.username}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0")


#---------------------------------------------------
class HotelRoom(models.Model):
    room_number = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description=models.CharField(max_length=200)
    status = models.CharField(
        max_length=50,
        choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Occupied', 'Occupied')],
        default='Available'
    )

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"
   
    
class HotelRevenue(models.Model):
    hotel_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.hotel_name
