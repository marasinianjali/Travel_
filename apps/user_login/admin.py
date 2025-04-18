
from django.contrib import admin
from .models import User, LoginAdmin, Wishlist, Trip, Notification, Booking, Language, Guide

# Custom admin configuration for the User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'status', 'dob', 'gender', 'theme', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('status', 'gender', 'theme')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, UserAdmin)

# Custom admin configuration for the LoginAdmin model
class LoginAdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')

admin.site.register(LoginAdmin, LoginAdminAdmin)

# Custom admin configuration for the Wishlist model
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination_name', 'added_at')
    search_fields = ('user__name', 'destination_name')
    list_filter = ('added_at',)

admin.site.register(Wishlist, WishlistAdmin)

# Custom admin configuration for the Trip model
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'start_date', 'end_date', 'status')
    search_fields = ('user__name', 'destination')
    list_filter = ('status', 'start_date', 'end_date')
    ordering = ('-start_date',)

admin.site.register(Trip, TripAdmin)

# Custom admin configuration for the Notification model
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notification_type', 'created_at', 'is_read')
    search_fields = ('user__name', 'message', 'notification_type')
    list_filter = ('notification_type', 'is_read', 'created_at')

admin.site.register(Notification, NotificationAdmin)

# Custom admin configuration for the Booking model
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'package', 'booking_date', 'status')
    search_fields = ('user__name', 'package__package_name')
    list_filter = ('status', 'booking_date')

admin.site.register(Booking, BookingAdmin)

# Custom admin configuration for the Language model
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Language, LanguageAdmin)

# Custom admin configuration for the Guide model
class GuideAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'rating', 'created_at', 'updated_at')
    search_fields = ('name', 'slug')
    list_filter = ('rating',)
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug from name

admin.site.register(Guide, GuideAdmin)
