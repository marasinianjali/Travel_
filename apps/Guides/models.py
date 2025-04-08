from django.db import models
from django.core.validators import MinValueValidator

class Guide(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    # Language Choices
    ENGLISH = 'English'
    NEPALI = 'Nepali'
    HINDI = 'Hindi'
    SPANISH = 'Spanish'
    FRENCH = 'French'
    CHINESE = 'Chinese'
    GERMAN = 'German'
    JAPANESE = 'Japanese'
    LANGUAGE_CHOICES = [
        (ENGLISH, 'English'),
        (NEPALI, 'Nepali'),
        (HINDI, 'Hindi'),
        (SPANISH, 'Spanish'),
        (FRENCH, 'French'),
        (CHINESE, 'Chinese'),
        (GERMAN, 'German'),
        (JAPANESE, 'Japanese'),
    ]

    # Location Choices (Country - City format)
    LOCATION_CHOICES = [
        ('Nepal - Kathmandu', 'Nepal - Kathmandu'),
        ('Nepal - Pokhara', 'Nepal - Pokhara'),
        ('Nepal - Chitwan', 'Nepal - Chitwan'),
        ('Nepal - Lumbini', 'Nepal - Lumbini'),
        ('India - Delhi', 'India - Delhi'),
        ('India - Mumbai', 'India - Mumbai'),
        ('India - Jaipur', 'India - Jaipur'),
        ('USA - New York', 'USA - New York'),
        ('USA - Los Angeles', 'USA - Los Angeles'),
        # Add more locations as needed
    ]

    guide_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, max_length=100, null=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        null=False
    )
    about_us = models.CharField(max_length=200, null=False)
    language = models.CharField(
        max_length=50,
        choices=LANGUAGE_CHOICES,
        null=False,
        default=NEPALI  # Optional: set a default language
    )
    payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        validators=[MinValueValidator(0.01)],
        db_column='amount'  # ✅ tells Django to use the 'amount' column
    )
    image = models.ImageField(upload_to='guides/', null=True, blank=True)
    location = models.CharField(
        max_length=100,
        choices=LOCATION_CHOICES,
        null=False,
        default='Nepal - Kathmandu'  # Optional: set a default location
    )
    phone = models.CharField(max_length=20, null=False)
    experience = models.IntegerField(null=False)
    expertise = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Guides'