from django.db import models
from django.contrib.auth.models import User 
from tour_package.models import TourPackage# If you want user-specific tracking



class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming tracking by user
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    conversion_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount} -{self.id}"

class ExpenseReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    tour_package = models.ForeignKey(TourPackage, related_name='expense_reports', on_delete=models.CASCADE)

    def __str__(self):
        return f"Report for {self.user.username} from {self.start_date} to {self.end_date}"
