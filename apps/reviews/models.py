from django.db import models
from django.contrib.auth.models import User
from apps.tourism_company.models import TourismCompany
from apps.tour_package.models import TourPackage
from apps.Guides.models import Guide
from apps.hotelbooking.models import HotelBooking
from django.core.validators import FileExtensionValidator
from fernet_fields import EncryptedCharField, EncryptedTextField, EncryptedDateTimeField

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)

    # User who created the review
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Reviewer",
        help_text="User who submitted the review."
    )

    # Related entities (all optional)
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name="Tour Package",
        help_text="Tour package being reviewed, if applicable."
    )
    guide = models.ForeignKey(
        Guide,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name="Guide",
        help_text="Guide being reviewed, if applicable."
    )
    hotel = models.ForeignKey(
        HotelBooking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name="Hotel Booking",
        help_text="Hotel booking being reviewed, if applicable."
    )
    company = models.ForeignKey(
        TourismCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name="Tourism Company",
        help_text="Tourism company being reviewed, if applicable."
    )

    # Review details
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Rating",
        help_text="Rating from 1 to 5 stars."
    )
    review_text = EncryptedTextField(
        blank=True,
        null=True,
        verbose_name="Review Text",
        help_text="Detailed review comments."
    )
    photo = models.ImageField(
        upload_to='reviews/',
        blank=True,
        null=True,
        verbose_name="Photo",
        help_text="Optional photo uploaded with the review (JPG/PNG only, max 5MB).",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Date and time when the review was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="Date and time when the review was last updated."
    )


    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"

    class Meta:
        db_table = 'Reviews'
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['company']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='valid_rating_range'
            ),
        ]
