from django.db import models
from fernet_fields import EncryptedCharField, EncryptedEmailField

class TourismCompany(models.Model):
    company_id = models.AutoField(
        primary_key=True,
        verbose_name="Company ID",
        help_text="Unique identifier for the tourism company."
    )
    user_name = models.CharField(
        max_length=100,
        verbose_name="User Name",
        help_text="Name of the user who owns the company."
    )
    user_phone = models.CharField(
        max_length=20,
        verbose_name="User Phone",
        help_text="Contact number of the user."
    )
    user_email = EncryptedEmailField(
        max_length=55,
       
        verbose_name="User Email",
        help_text="Email of the user (must be unique)."
    )
    company_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Company Name",
        help_text="Name of the tourism company."
    )
    company_phone = models.CharField(
        max_length=20,
        verbose_name="Company Phone",
        help_text="Contact number of the company."
    )
    company_address = EncryptedCharField(
        max_length=255,
        verbose_name="Company Address",
        help_text="Address of the company."
    )
    password = models.CharField(
        max_length=128,
        verbose_name="Password",
        help_text="Password for the company account (should be hashed)."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active",
        help_text="Indicates whether the company account is active."
    )

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Tourism Company"
        verbose_name_plural = "Tourism Companies"
        db_table = "tourism_company_tourismcompany"
