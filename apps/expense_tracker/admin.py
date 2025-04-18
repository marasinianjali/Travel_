from django.contrib import admin
from .models import ExpenseCategory, Expense, ExpenseReport

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'date', 'user', 'tour_package')
    search_fields = ('category__name', 'description', 'user__username')
    list_filter = ('category', 'date', 'user', 'tour_package')
    date_hierarchy = 'date'
    ordering = ('-date',)  # Changed from '-created_at'

@admin.register(ExpenseReport)
class ExpenseReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'total_expenses', 'tour_package')
    search_fields = ('user__username', 'tour_package__name')
    list_filter = ('start_date', 'end_date', 'user', 'tour_package')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)  # Changed from '-created_at'