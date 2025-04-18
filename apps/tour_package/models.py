from django.db import models


class TourPackage(models.Model):
    package_id = models.AutoField(
        primary_key=True,
        verbose_name="Package ID",
        help_text="Unique identifier for the tour package."
    )
    package_name = models.CharField(
        max_length=255,
        verbose_name="Package Name",
        help_text="Name of the tour package."
    )
    company = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Company",
        help_text="Name of the tourism company offering this package."
    )
    date = models.DateField(
        verbose_name="Date",
        help_text="Date the tour package is scheduled for."
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Detailed description of the tour package."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Amount",
        help_text="Price of the tour package."
    )
    duration = models.IntegerField(
        verbose_name="Duration (Days)",
        help_text="Duration of the tour package in days."
    )
    country = models.CharField(
        max_length=255,
        verbose_name="Country",
        help_text="Country where the tour takes place."
    )
    city = models.CharField(
        max_length=255,
        verbose_name="City",
        help_text="City where the tour takes place."
    )
    tour_type = models.CharField(
        max_length=255,
        verbose_name="Tour Type",
        help_text="Type of tour (e.g., Adventure, Family, Cultural)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the tour package was created."
    )

    def __str__(self):
        return self.package_name

    class Meta:
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"
        db_table = "tour_packages"
