from django.db import models

class TourismCompany(models.Model):  # Assuming this is your company model
    name = models.CharField(max_length=255)  

class TourPackage(models.Model):
    package_id = models.AutoField(primary_key=True)
    package_name = models.CharField(max_length=255)
    company = models.ForeignKey(TourismCompany, on_delete=models.CASCADE)  # Fix this!
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    tour_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Add this field for approval

    def __str__(self):
        return self.package_name

    class Meta:
        db_table = 'TourPackage'    