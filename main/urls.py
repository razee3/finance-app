from django.urls import path
from .views import dashboard_view, transaction_list, add_transaction, edit_transaction, delete_transaction, get_category_options

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('transactions/add/', add_transaction, name='add_transaction'),
    path('transactions/edit/<int:pk>/',
         edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:pk>/',
         delete_transaction, name='delete_transaction'),
    path('get-category-options/', get_category_options, name='get_category_options'),
    # path('analysis/income/', income_analysis, name='income_analysis'),
    # path('analysis/expense/', expense_analysis, name='expense_analysis'),
]
