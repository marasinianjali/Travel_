
from django.contrib import admin
from .models import Location, Language

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'rating')
    search_fields = ('name', 'languages__name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('languages', 'rating')

admin.site.register(Location, LocationAdmin)
admin.site.register(Language)
