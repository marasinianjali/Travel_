from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'user', 'rating', 'package', 'guide', 'hotel', 'company')
    search_fields = ('user__username', 'review_text', 'package__name', 'company__name')
    list_filter = ('rating', 'created_at', 'package', 'guide', 'hotel', 'company')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('review_id',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'package', 'guide', 'hotel', 'company')