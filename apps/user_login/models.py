
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.tour_package.models import TourPackage  # Importing TourPackage model


# Abstract Base Class for common fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LoginAdmin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'LoginAdmin'


class User(models.Model):
    STATUS_CHOICES = [
        ('married', 'Married'),
        ('unmarried', 'Unmarried'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, verbose_name="User Name", help_text="Enter the user's full name.")
    email = models.EmailField(max_length=55, unique=True, null=False, verbose_name="Email Address", help_text="Enter a valid email address.")
    password = models.CharField(max_length=255, null=False, verbose_name="Password", help_text="Password will be hashed before saving.")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number", help_text="Enter a phone number.")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address", help_text="Enter user's address.")
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True, verbose_name="Gender")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='married', verbose_name="Marital Status")
    dob = models.DateField(null=False, verbose_name="Date of Birth", help_text="Enter user's date of birth.")
    bio = models.TextField(blank=True, null=True, verbose_name="Biography", help_text="User's bio for profile.")
    theme = models.CharField(max_length=50, default='light', choices=[('light', 'Light'), ('dark', 'Dark')], verbose_name="Theme", help_text="Choose the preferred theme.")
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'User'


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination_name = models.CharField(max_length=100, verbose_name="Destination Name", help_text="Enter the destination name.")
    description = models.TextField(blank=True, null=True, verbose_name="Description", help_text="Enter a description of the destination.")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.destination_name}"
    
    class Meta:
        db_table = 'Wishlist'


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100, verbose_name="Destination Name", help_text="Enter the destination of the trip.")
    start_date = models.DateField(verbose_name="Start Date", help_text="Enter the trip start date.")
    end_date = models.DateField(verbose_name="End Date", help_text="Enter the trip end date.")
    status = models.CharField(max_length=20, choices=[('planned', 'Planned'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='planned', verbose_name="Trip Status")

    def __str__(self):
        return f"{self.user.name} - {self.destination}"

    class Meta:
        db_table = 'Trip'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Notification Message", help_text="Enter the notification message.")
    notification_type = models.CharField(max_length=50, choices=[('deal', 'Deal'), ('flight', 'Flight Change'), ('safety', 'Safety Update')], verbose_name="Notification Type")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.message[:20]}"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="user_bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Cancelled", "Cancelled")], default="Pending")

    def __str__(self):
        return f"Booking {self.booking_id} - {self.package.package_name}"

    class Meta:
        db_table = 'Booking'


# New Language Model for normalization
class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Language Name", help_text="Enter the name of the language.")
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Language'


# Guide model with Many-to-Many for languages, slug, profile picture, and rating
class Guide(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Guide Name", help_text="Enter the guide's name.")
    slug = models.SlugField(unique=True, blank=True, help_text="SEO-friendly URL slug.")
    profile_picture = models.ImageField(upload_to='guide_profiles/', blank=True, help_text="Upload profile picture.")
    languages = models.ManyToManyField(Language, related_name="guides", blank=True, verbose_name="Languages", help_text="Languages spoken by the guide.")
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], verbose_name="Rating", help_text="Rating of the guide (0-5).")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")  # Auto-generate slug from name if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Guide'
        verbose_name = "Tour Guide"
        verbose_name_plural = "Tour Guides" 

