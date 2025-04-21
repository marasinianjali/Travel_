from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import bleach

class Location(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Location Name",
        help_text="Enter the name of the location, e.g., City or Landmark."
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name="Latitude",
        help_text="Latitude of the location. Must be between -90 and 90."
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name="Longitude",
        help_text="Longitude of the location. Must be between -180 and 180."
    )
    languages = models.ManyToManyField(
        'Language',
        related_name='locations',
        blank=True,
        verbose_name="Languages Spoken",
        help_text="Languages spoken in this location. Choose from available languages."
    )
    slug = models.SlugField(
        unique=True, 
        blank=True, 
        editable=False,
        verbose_name="Location Slug",
        help_text="URL-friendly version of the location's name for SEO purposes."
    )
    profile_picture = models.ImageField(
        upload_to='location_profiles/',
        blank=True,
        verbose_name="Profile Picture",
        help_text="Upload an image representing the location."
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name="Rating",
        help_text="Rating of the location, on a scale of 0 to 5."
    )

    def __str__(self):
        return self.name

    def get_static_map_url(self):
        """Generates a Geoapify static map URL."""
        api_key = "YOUR_API_KEY"
        return f"https://maps.geoapify.com/v1/staticmap?style=osm-bright&width=600&height=400&center=lonlat:{self.longitude},{self.latitude}&zoom=12&apiKey={api_key}"

    def clean(self):
        """Model-level validation & sanitization (against XSS)."""
        if not self.name:
            raise ValidationError("Location name is required.")
        if not (self.latitude and self.longitude):
            raise ValidationError("Latitude and Longitude are required.")

        # XSS protection for 'name' field
        clean_name = bleach.clean(self.name, tags=[], attributes={}, strip=True)
        self.name = strip_tags(clean_name)

    def save(self, *args, **kwargs):
        """Override save to sanitize input and auto-generate slug."""
        self.full_clean()  # Calls clean() to sanitize input
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Language Name",
        help_text="The name of the language."
    )

    def __str__(self):
        return self.name

    def clean(self):
        """Sanitize name to prevent XSS."""
        clean_name = bleach.clean(self.name, tags=[], attributes={}, strip=True)
        self.name = strip_tags(clean_name)

    def save(self, *args, **kwargs):
        self.full_clean()  # Sanitizes input
        super().save(*args, **kwargs)
