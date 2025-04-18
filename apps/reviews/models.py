from django.db import models


class TourismCompany(models.Model):
    company_id = models.AutoField(primary_key=True)

    # User Details
    user_name = models.CharField(
        max_length=100,
        verbose_name="User Name",
        help_text="Name of the person managing the company account."
    )
    user_phone = models.CharField(
        max_length=20,
        verbose_name="User Phone",
        help_text="Contact number of the user."
    )
    user_email = models.EmailField(
        max_length=55,
        unique=True,
        verbose_name="User Email",
        help_text="Email address of the user (used for login)."
    )

    # Company Details
    company_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Company Name",
        help_text="Unique name of the tourism company."
    )
    company_phone = models.CharField(
        max_length=20,
        verbose_name="Company Phone",
        help_text="Phone number of the tourism company."
    )
    company_address = models.CharField(
        max_length=255,
        verbose_name="Company Address",
        help_text="Physical address of the tourism company."
    )

    # Authentication & Status
    password = models.CharField(
        max_length=128,
        verbose_name="Password",
        help_text="Password for the company account."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Indicates whether the account is active."
    )

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'TourismCompany'
        verbose_name = "Tourism Company"
        verbose_name_plural = "Tourism Companies"
