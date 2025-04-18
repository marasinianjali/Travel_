from django import forms
from django.core.validators import MinValueValidator
from .models import Expense, ExpenseCategory, ExpenseReport


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Category name must be at least 2 characters long.")
        return name


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            "user",
            "category",
            "amount",
            "date",
            "description",
            "conversion_rate",
            "tour_package",
        ]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "conversion_rate": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.0001"}
            ),
            "tour_package": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean_conversion_rate(self):
        conversion_rate = self.cleaned_data.get("conversion_rate")
        if conversion_rate <= 0:
            raise forms.ValidationError("Conversion rate must be greater than zero.")
        return conversion_rate


class ExpenseReportForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = ["user", "start_date", "end_date", "total_expenses", "tour_package"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "total_expenses": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "tour_package": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        total_expenses = cleaned_data.get("total_expenses")

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be before end date.")
        if total_expenses is not None and total_expenses < 0:
            raise forms.ValidationError("Total expenses cannot be negative.")
        return cleaned_data