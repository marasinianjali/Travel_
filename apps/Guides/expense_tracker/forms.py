from django import forms
from .models import Expense, ExpenseCategory, ExpenseReport

# Form for Expense
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['user', 'category', 'amount', 'date', 'description', 'conversion_rate', 'tour_package']

# Form for ExpenseCategory
class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']

# Form for ExpenseReport
class ExpenseReportForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = ['user', 'start_date', 'end_date', 'total_expenses', 'tour_package']
