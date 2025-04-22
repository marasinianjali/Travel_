from django.db import models

from django.db import models
from fernet_fields import EncryptedCharField
from fernet_fields import EncryptedField
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    payment_id = models.AutoField(primary_key=True)
    booking_id = models.IntegerField(unique=True)
    hotel_id = models.IntegerField(null=True, blank=True)
    guide_id = models.IntegerField(null=True, blank=True)
    
    name = EncryptedCharField(max_length=255)
    hotel_name = EncryptedCharField(max_length=255)
    phone_number = EncryptedCharField(max_length=20)
    amount = EncryptedDecimalField(default=1000.00,  
        validators=[MinValueValidator(0.01)],)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"


# Create your models here.
