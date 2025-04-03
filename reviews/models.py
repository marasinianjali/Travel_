from django.db import models
from django.contrib.auth.models import User
from tourism_company.models import TourismCompany
from tour_package.models import TourPackage
from Guides.models import Guide
from hotelbooking.models import HotelBooking

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, null=True, blank=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(TourismCompany, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating between 1-5
    review_text = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} stars"

