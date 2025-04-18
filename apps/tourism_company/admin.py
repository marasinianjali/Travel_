from django.contrib import admin
from .models import TourismCompany

@admin.register(TourismCompany)
class TourismCompanyAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'company_phone',
        'company_address',
        'user_name',
        'user_phone',
        'user_email',
    )
    search_fields = ('company_name', 'user_name', 'user_email')
    list_filter = ('company_address',)

    fieldsets = (
        ('Company Info', {
            'fields': ('company_name', 'company_phone', 'company_address')
        }),
        ('Contact Person Info', {
            'fields': ('user_name', 'user_phone', 'user_email')
        }),
    )
