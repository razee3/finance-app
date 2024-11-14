import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
from django.http import HttpResponseForbidden
from django.db import models
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.


def home_view(request):
    return render(request, 'home.html')


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(
        user=request.user).order_by('-date')
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'transactions/transaction_list.html', {'page_obj': page_obj})


@login_required
def add_transaction(request):

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'transactions/add_transaction.html', {form: form})


def get_category_options(request):
    profile = request.user.profile
    transaction_type = request.GET.get('type')
    
    if transaction_type == 'income':
        categories = [category for category in profile.income_categories.split(',')]
    else:
        categories = [category for category in profile.expense_categories.split(',')]
    
    return JsonResponse({'categories': categories})


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # Ensure the logged-in user is the owner of the transaction
    if transaction.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this transaction.")

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction_form.html', {'form': form})


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    # Ensure the logged-in user is the owner of the transaction
    if transaction.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this transaction.")

    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})


@login_required
def dashboard_view(request):
    # Get date range from the request (if available)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filter transactions by the logged-in user
    transactions = Transaction.objects.filter(user=request.user)

    # Apply date range filtering if dates are provided
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Calculate total income and expenses
    total_income = transactions.filter(transaction_type='income').aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    total_expenses = transactions.filter(transaction_type='expense').aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0

    # Calculate the total number of transactions
    total_transactions = transactions.count()

    # Calculate the balance
    balance = total_income - total_expenses

    income_category_totals = transactions.filter(transaction_type='income').values('category').annotate(
        total=models.Sum('amount'))
    
    for category in income_category_totals:
        category['percentage'] = (category['total'] / total_income) * 100

    expense_category_totals = transactions.filter(transaction_type='expense').values('category').annotate(
        total=models.Sum('amount'))
    
    for category in expense_category_totals:
        category['percentage'] = (category['total'] / total_expenses) * 100

    
    # Pass the calculated values and date range to the template
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_transactions': total_transactions,
        'balance': balance,
        'start_date': start_date,
        'end_date': end_date,
        'income_category_totals': income_category_totals,
        'expense_category_totals': expense_category_totals,
        'income_data_empty': len(income_category_totals) == 0,
        'expense_data_empty': len(expense_category_totals) == 0,
    }

    return render(request, 'dashboard.html', context)

