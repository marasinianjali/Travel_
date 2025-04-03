from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

    def get_static_map_url(self):
        """Generates a Geoapify static map URL."""
        api_key = "YOUR_API_KEY"
        return f"https://maps.geoapify.com/v1/staticmap?style=osm-bright&width=600&height=400&center=lonlat:{self.longitude},{self.latitude}&zoom=12&apiKey={api_key}"
