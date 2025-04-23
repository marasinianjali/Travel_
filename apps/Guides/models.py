from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from django.core.exceptions import ValidationError
from fernet_fields import EncryptedCharField, EncryptedTextField, EncryptedDateTimeField, EncryptedEmailField
from django.utils.text import slugify

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


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

# Abstract base model for common fields

class BasePerson(models.Model):
    name = EncryptedCharField(
        max_length=100,
       
        verbose_name="Full Name",
        help_text="Enter the full name."
    )
    email = EncryptedEmailField(
        max_length=100,
        verbose_name="Email Address",
        help_text="Enter a valid and unique email."
    )
    phone = EncryptedCharField(
        max_length=20,
        verbose_name="Phone Number",
        help_text="Enter a valid contact number.",
        validators=[RegexValidator(r'^\+?\d{7,15}$', message="Enter a valid phone number.")]
    )

    class Meta:
        abstract = True


class Language(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Language",
        help_text="Name of the spoken language."
    )

    def __str__(self):
        return self.name


class Guide(BasePerson):
    guide_id = models.AutoField(primary_key=True) 
    
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

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
    ]

    
    dob = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Birth",
        help_text="Enter the guide's birth date."
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        verbose_name="Gender",
        help_text="Select the guide's gender."
    )
    about_us = EncryptedCharField(
        max_length=200,
        verbose_name="About the Guide",
        help_text="Brief summary about the guide."
    )
    languages = models.ManyToManyField(
        to='Language',
        verbose_name="Languages Spoken",
        help_text="Comma-separated languages spoken by the guide."

    )
    location = models.CharField(
        max_length=100,
        choices=LOCATION_CHOICES,
        verbose_name="Base Location",
        help_text="Select the guide's operating location."
    )
    experience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        verbose_name="Years of Experience",
        help_text="Number of years the guide has been active (0–60)."
    )
    expertise = EncryptedTextField(
        verbose_name="Areas of Expertise",
        help_text="Enter the guide's key strengths, regions, or specialties."
    )
    amount = EncryptedDecimalField(
        
        default=1000.00,  
        validators=[MinValueValidator(0.01)],
        verbose_name="Payment Rate",
        help_text="Set the standard rate per assignment."
    )
   
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name="Profile Image",
        help_text="Guide's image stored as binary data."
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name="Rating",
        help_text="Average rating (0.0–5.0) from reviews."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp of when the guide was added."
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        unique=False,
        help_text="Auto-generated slug from name"
    )
    def __str__(self):
        return self.name

    def clean(self):
        # Example model-level validation
        if self.experience < 0 or self.experience > 60:
            raise ValidationError("Experience must be between 0 and 60 years.")
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0.0 and 5.0.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Guides'
        verbose_name = "Tour Guide"
        verbose_name_plural = "Tour Guides"



# Custom user manager
class UserBaseManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, phone, password, **extra_fields)


# Custom user model
class UserBase(BasePerson, AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserBaseManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__ (self):
        return self.email

    class Meta:
        db_table = 'UserBase'
        verbose_name = "User"
        verbose_name_plural = "Users"