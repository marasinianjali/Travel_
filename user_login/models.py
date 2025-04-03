from django.db import models
from django.contrib.auth.hashers import make_password

from tour_package.models import TourPackage  # Importing TourPackage model

class LoginAdmin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
    # class Meta:
    #     db_table: 'Admin'



class User(models.Model):
    STATUS_CHOICES = [
        ('married', 'Married'),
        ('unmarried', 'Unmarried'),
    ]
    
    # Use user_id as the primary key to match the MySQL table
    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=55, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)  # Will be hashed
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='married')
    dob = models.DateField(null=False)
    # New fields for profile customization
    bio = models.TextField(blank=True, null=True)
    theme = models.CharField(max_length=50, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])  # Example themes

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # Prevent re-hashing on updates
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'User'  # Match the MySQL table name






# New Model for Saved Destinations/Wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.destination_name}"
    
    class Meta:
        db_table = 'Wishlist'


# New Model for Trip Progress Tracker
class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='planned')

    def __str__(self):
        return f"{self.user.name} - {self.destination}"
    
    class Meta:
        db_table = 'Trip'

# New Model for Notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[('deal', 'Deal'), ('flight', 'Flight Change'), ('safety', 'Safety Update')])
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.message[:20]}"



#--------------THIS model is for users to book a tour package which is link
#-------------- to views inside tour_package.views
class Booking(models.Model):

     # user_id = models.IntegerField()  # Assuming session-based user IDs
     # user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    # 
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="user_bookings")  # Use related_name
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled")
    ], default="Pending")

    def __str__(self):
        return f"Booking {self.booking_id} - {self.package.package_name}"
    
    