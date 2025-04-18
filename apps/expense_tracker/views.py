from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Expense, ExpenseCategory, ExpenseReport
from .forms import ExpenseForm, ExpenseCategoryForm, ExpenseReportForm


# Custom test function to check if the user is an admin
def is_admin(user):
    return user.is_superuser or hasattr(user, "loginadmin")


# List all expense categories (limited to 10)
def expense_category_list(request):
    query = request.GET.get("search", "")
    if query:
        categories = ExpenseCategory.objects.filter(name__icontains=query)[:10]
    else:
        categories = ExpenseCategory.objects.all()[:10]
    return render(
        request,
        "expense_tracker/expense_category_list.html",
        {"categories": categories},
    )


# Create expense category - admin only
@login_required
@user_passes_test(is_admin)
def create_expense_category(request):
    if request.method == "POST":
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense category created successfully!")
            return redirect("expense_tracker:expense_category_list")
        else:
            return render(
                request,
                "expense_tracker/create_expense_category.html",
                {"form": form},
            )
    else:
        form = ExpenseCategoryForm()
    return render(
        request, "expense_tracker/create_expense_category.html", {"form": form}
    )


# Update expense category - admin only
@login_required
@user_passes_test(is_admin)
def update_expense_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    form = ExpenseCategoryForm(request.POST or None, instance=category)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Expense category updated successfully!")
            return redirect("expense_tracker:expense_category_list")
        else:
            return render(
                request,
                "expense_tracker/create_expense_category.html",
                {"form": form, "category": category},
            )
    return render(
        request,
        "expense_tracker/create_expense_category.html",
        {"form": form, "category": category},
    )


# Delete expense category - admin only
@login_required
@user_passes_test(is_admin)
def delete_expense_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Expense category deleted successfully!")
        return redirect("expense_tracker:expense_category_list")
    return render(
        request,
        "expense_tracker/expense_category_confirm_delete.html",
        {"category": category},
    )


# List all expenses (limited to 10)
def expense_list(request):
    query = request.GET.get("search", "")
    if query:
        expenses = Expense.objects.filter(description__icontains=query)[:10]
    else:
        expenses = Expense.objects.all()[:10]
    return render(
        request, "expense_tracker/expense_list.html", {"expenses": expenses}
    )


# Create expense - admin only
@login_required
@user_passes_test(is_admin)
def create_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense created successfully!")
            return redirect("expense_tracker:expense_list")
        else:
            return render(
                request, "expense_tracker/create_expense.html", {"form": form}
            )
    else:
        form = ExpenseForm()
    return render(
        request, "expense_tracker/create_expense.html", {"form": form}
    )


# Update expense - admin only
@login_required
@user_passes_test(is_admin)
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(request.POST or None, instance=expense)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect("expense_tracker:expense_list")
        else:
            return render(
                request,
                "expense_tracker/create_expense.html",
                {"form": form, "expense": expense},
            )
    return render(
        request,
        "expense_tracker/create_expense.html",
        {"form": form, "expense": expense},
    )


# Delete expense - admin only
@login_required
@user_passes_test(is_admin)
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
        return redirect("expense_tracker:expense_list")
    return render(
        request,
        "expense_tracker/expense_confirm_delete.html",
        {"expense": expense},
    )


# List all expense reports (limited to 10)
def expense_report_list(request):
    query = request.GET.get("search", "")
    if query:
        reports = ExpenseReport.objects.filter(user__username__icontains=query)[:10]
    else:
        reports = ExpenseReport.objects.all()[:10]
    return render(
        request, "expense_tracker/expense_report_list.html", {"reports": reports}
    )


# View single expense report
def view_expense_report(request, pk):
    report = get_object_or_404(ExpenseReport, pk=pk)
    return render(
        request, "expense_tracker/view_expense_report.html", {"report": report}
    )


# Create expense report - admin only
@login_required
@user_passes_test(is_admin)
def create_expense_report(request):
    if request.method == "POST":
        form = ExpenseReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense report created successfully!")
            return redirect("expense_tracker:expense_report_list")
        else:
            return render(
                request,
                "expense_tracker/create_expense_report.html",
                {"form": form},
            )
    else:
        form = ExpenseReportForm()
    return render(
        request, "expense_tracker/create_expense_report.html", {"form": form}
    )


# Update expense report - admin only
@login_required
@user_passes_test(is_admin)
def update_expense_report(request, pk):
    report = get_object_or_404(ExpenseReport, pk=pk)
    form = ExpenseReportForm(request.POST or None, instance=report)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Expense report updated successfully!")
            return redirect("expense_tracker:expense_report_list")
        else:
            return render(
                request,
                "expense_tracker/create_expense_report.html",
                {"form": form, "report": report},
            )
    return render(
        request,
        "expense_tracker/create_expense_report.html",
        {"form": form, "report": report},
    )


# Delete expense report - admin only
@login_required
@user_passes_test(is_admin)
def delete_expense_report(request, pk):
    report = get_object_or_404(ExpenseReport, pk=pk)
    if request.method == "POST":
        report.delete()
        messages.success(request, "Expense report deleted successfully!")
        return redirect("expense_tracker:expense_report_list")
    return render(
        request,
        "expense_tracker/expense_report_confirm_delete.html",
        {"report": report},
    )