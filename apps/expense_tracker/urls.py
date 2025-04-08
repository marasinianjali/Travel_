from django.urls import path
from . import views

app_name = 'expense_tracker'

urlpatterns = [
    path('expense/create/', views.create_expense, name='create_expense'),
    path('expense/list/', views.expense_list, name='expense_list'),
    path('expense/update/<int:pk>/', views.update_expense, name='update_expense'),
    path('expense/delete/<int:pk>/', views.delete_expense, name='delete_expense'),

    path('category/create/', views.create_expense_category, name='create_expense_category'),
    path('category/list/', views.expense_category_list, name='expense_category_list'),
    path('category/update/<int:pk>/', views.update_expense_category, name='update_expense_category'),
    path('category/delete/<int:pk>/', views.delete_expense_category, name='delete_expense_category'),

    path('report/create/', views.create_expense_report, name='create_expense_report'),
    path('report/list/', views.expense_report_list, name='expense_report_list'),
    path('expense-reports/', views.expense_report_list, name='expense_report_list'),
    path('expense-report/create/', views.create_expense_report, name='create_expense_report'),
    path('expense-report/<int:pk>/update/', views.update_expense_report, name='update_expense_report'),
    path('expense-report/<int:pk>/delete/', views.delete_expense_report, name='delete_expense_report'),
    path('expense-report/<int:pk>/', views.view_expense_report, name='view_expense_report'),

]

