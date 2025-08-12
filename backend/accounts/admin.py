# accounts/admin.py
from django.contrib import admin
from .models import Agent
from transactions.models import Transaction
import decimal

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'operational_credit', 'is_staff')
    search_fields = ('username', 'email')
    fields = ('username', 'email', 'operational_credit', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    readonly_fields = ('last_login', 'date_joined')

    def save_model(self, request, obj, form, change):
        # 'change' is True if editing an existing object
        if change:
            try:
                original_obj = Agent.objects.get(pk=obj.pk)
                original_credit = original_obj.operational_credit
            except Agent.DoesNotExist:
                super().save_model(request, obj, form, change)
                return

            new_credit = obj.operational_credit
            
            if new_credit != original_credit:
                adjustment = new_credit - original_credit
                
                transaction_type = Transaction.TransactionType.ADMIN_CREDIT if adjustment > 0 else Transaction.TransactionType.ADMIN_DEBIT
                
                Transaction.objects.create(
                    agent=obj,
                    transaction_type=transaction_type,
                    amount=abs(adjustment),
                    balance_after_transaction=new_credit,
                    notes=f"Manual adjustment by admin: {request.user.username}"
                )
        
        super().save_model(request, obj, form, change)```

#### **`backend/api/serializers.py`**

```python
# api/serializers.py
from rest_framework import serializers
from accounts.models import Agent
from games.models import GameRound, GameSpeed, WinningPattern
from transactions.models import Transaction

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'username', 'email', 'operational_credit']

class GameSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSpeed
        fields = '__all__'

class WinningPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinningPattern
        fields = '__all__'

class GameRoundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRound
        fields = ['game_speed', 'winning_pattern', 'card_price', 'commission_percentage']

class GameRoundDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRound
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    # Format amount to be signed (+/-)
    signed_amount = serializers.SerializerMethodField()
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'timestamp', 'transaction_type', 'transaction_type_display', 'signed_amount', 'balance_after_transaction', 'notes']

    def get_signed_amount(self, obj):
        if obj.transaction_type in [Transaction.TransactionType.ADMIN_DEBIT, Transaction.TransactionType.GAME_LAUNCH]:
            return -obj.amount
        return obj.amount