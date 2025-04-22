from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.tour_package.models import TourPackage
from fernet_fields import EncryptedCharField, EncryptedTextField, EncryptedDateTimeField


class ExpenseCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name",
        help_text="Enter the name of the expense category (e.g., Food, Transport)."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"
        db_table = "expense_tracker_expensecategory"


class Expense(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="Select the user associated with this expense."
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.CASCADE,
        verbose_name="Category",
        help_text="Select the expense category."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Amount",
        help_text="Enter the expense amount (e.g., 50.00)."
    )
    date = models.DateField(
        verbose_name="Expense Date",
        help_text="Select the date the expense was incurred."
    )
    description = EncryptedTextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Optional description of the expense."
    )
    conversion_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=1.0,
        validators=[MinValueValidator(0.0001)],
        verbose_name="Conversion Rate",
        help_text="Currency conversion rate (e.g., 1.0 for no conversion)."
    )
    tour_package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Tour Package",
        help_text="Optional associated tour package."
    )

    def __str__(self):
        return f"{self.category.name} - {self.amount} (ID: {self.id})"

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        if self.conversion_rate <= 0:
            raise ValidationError("Conversion rate must be greater than zero.")

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        db_table = "expense_tracker_expense"


class ExpenseReport(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        help_text="Select the user who generated this report."
    )
    start_date = models.DateField(
        verbose_name="Start Date",
        help_text="Select the start date of the report period."
    )
    end_date = models.DateField(
        verbose_name="End Date",
        help_text="Select the end date of the report period."
    )
    total_expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        verbose_name="Total Expenses",
        help_text="Total expenses for the report period."
    )
    tour_package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name="expense_reports",
        verbose_name="Tour Package",
        help_text="Associated tour package for this report."
    )

    def __str__(self):
        return f"Report for {self.user.username} ({self.start_date} to {self.end_date})"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")
        if self.total_expenses < 0:
            raise ValidationError("Total expenses cannot be negative.")

    class Meta:
        verbose_name = "Expense Report"
        verbose_name_plural = "Expense Reports"
        db_table = "expense_tracker_expensereport"