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

    guide_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, max_length=100, null=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        null=False  # Changed to match SQL
    )
    about_us = models.CharField(max_length=200, null=False)  # Changed to match SQL
    language = models.CharField(max_length=255, null=False)  # Changed to match SQL
    payment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        validators=[MinValueValidator(0.01)]  # To match CHECK (amount > 0)
    )
    image = models.BinaryField(null=True, blank=True)
    location = models.CharField(max_length=255, null=False)  # Changed to match SQL
    phone = models.CharField(max_length=20, null=False)  # Changed to match SQL
    experience = models.IntegerField(null=False)  # Changed to match SQL
    expertise = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name