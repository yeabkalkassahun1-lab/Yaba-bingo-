# transactions/models.py
from django.db import models
from accounts.models import Agent

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        ADMIN_CREDIT = 'ADMIN_CREDIT', 'Admin Credit'
        ADMIN_DEBIT = 'ADMIN_DEBIT', 'Admin Debit'
        GAME_LAUNCH = 'GAME_LAUNCH', 'Game Launch Cost'

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='transactions')
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Always positive, type defines direction
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_transaction_type_display()} for {self.agent.username} at {self.timestamp}"