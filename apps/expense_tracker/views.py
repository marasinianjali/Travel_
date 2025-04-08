from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Expense, ExpenseCategory, ExpenseReport
from .forms import ExpenseForm, ExpenseCategoryForm, ExpenseReportForm
from django.http import HttpResponse

# Create Expense
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense created successfully!')
            return redirect('expense_tracker:expense_list')  # Redirect to expense list page
    else:
        form = ExpenseForm()
    return render(request, 'expense_tracker/create_expense.html', {'form': form})

# List Expenses
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_tracker/expense_list.html', {'expenses': expenses})

# Update Expense
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_tracker:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_tracker/create_expense.html', {'form': form})

# Delete Expense
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('expense_tracker:expense_list')

# Create ExpenseCategory
def create_expense_category(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense Category created successfully!')
            return redirect('expense_tracker:expense_category_list')
    else:
        form = ExpenseCategoryForm()
    return render(request, 'expense_tracker/create_expense_category.html', {'form': form})

# List Expense Categories
def expense_category_list(request):
    categories = ExpenseCategory.objects.all()
    return render(request, 'expense_tracker/expense_category_list.html', {'categories': categories})

# Update ExpenseCategory
def update_expense_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense Category updated successfully!')
            return redirect('expense_tracker:expense_category_list')
    else:
        form = ExpenseCategoryForm(instance=category)
    return render(request, 'expense_tracker/create_expense_category.html', {'form': form})

# Delete ExpenseCategory
def delete_expense_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    category.delete()
    messages.success(request, 'Expense Category deleted successfully!')
    return redirect('expense_tracker:expense_category_list')

# Create Expense Report
def create_expense_report(request):
    if request.method == 'POST':
        form = ExpenseReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense Report created successfully!')
            return redirect('expense_tracker:expense_report_list')
    else:
        form = ExpenseReportForm()
    return render(request, 'expense_tracker/create_expense_report.html', {'form': form})

# List Expense Reports
def expense_report_list(request):
    reports = ExpenseReport.objects.all()
    return render(request, 'expense_tracker/expense_report_list.html', {'reports': reports})

# Update Expense Report
def update_expense_report(request, pk):
    report = get_object_or_404(ExpenseReport, pk=pk)
    if request.method == 'POST':
        form = ExpenseReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense Report updated successfully!')
            return redirect('expense_tracker:expense_report_list')
    else:
        form = ExpenseReportForm(instance=report)
    return render(request, 'expense_tracker/create_expense_report.html', {'form': form, 'report': report})

# Delete Expense Report
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ExpenseReport

def delete_expense_report(request, pk):
    # Get the expense report or return 404 if not found
    report = get_object_or_404(ExpenseReport, pk=pk)

    # Check if the request method is POST, which means the user confirmed deletion
    if request.method == 'POST':
        # Delete the expense report
        report.delete()

        # Display a success message
        messages.success(request, 'Expense Report deleted successfully!')

        # Redirect to the list of expense reports
        return redirect('expense_tracker:expense_report_list')

    # If the request is GET, show the confirmation page
    return render(request, 'expense_tracker/delete_expense_report.html', {'report': report})
def view_expense_report(request, pk):
    report = get_object_or_404(ExpenseReport, pk=pk)
    return render(request, 'expense_tracker/view_expense_report.html', {'report': report})
