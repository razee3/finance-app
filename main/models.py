from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    transaction_type = models.CharField(
        max_length=7, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.transaction_type})"
