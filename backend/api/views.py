# api/views.py
from rest_framework import generics, permissions, views, response, status
from rest_framework.exceptions import ValidationError
from django.db import transaction as db_transaction
import random

from .serializers import (
    AgentSerializer, TransactionSerializer, GameSpeedSerializer, 
    WinningPatternSerializer, GameRoundCreateSerializer, GameRoundDetailSerializer
)
from accounts.models import Agent
from transactions.models import Transaction
from games.models import GameRound, GameSpeed, WinningPattern

# --- Utility Function ---
def generate_boards(count=100):
    boards = set()
    while len(boards) < count:
        board = []
        ranges = {'B': (1, 15), 'I': (16, 30), 'N': (31, 45), 'G': (46, 60), 'O': (61, 75)}
        for col_letter, (start, end) in ranges.items():
            col_nums = random.sample(range(start, end + 1), 5)
            board.extend(col_nums)
        # Add free space marker (index 12 is the center)
        board[12] = "FREE"
        boards.add(tuple(board))
    return [list(b) for b in boards]

# --- API Views ---
class AgentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AgentSerializer
    def get_object(self):
        return self.request.user

class TransactionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    def get_queryset(self):
        return Transaction.objects.filter(agent=self.request.user)

class GameOptionsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        speeds = GameSpeed.objects.all()
        patterns = WinningPattern.objects.all()
        return response.Response({
            'speeds': GameSpeedSerializer(speeds, many=True).data,
            'patterns': WinningPatternSerializer(patterns, many=True).data
        })

class GameRoundCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GameRoundCreateSerializer

    def perform_create(self, serializer):
        agent = self.request.user
        validated_data = serializer.validated_data
        
        # Core Economic Logic
        card_price = validated_data['card_price']
        total_cards = 100 # Fixed
        commission = validated_data['commission_percentage']
        
        total_potential_revenue = card_price * total_cards
        agent_commission_amount = (total_potential_revenue * commission) / 100
        game_launch_cost = total_potential_revenue - agent_commission_amount

        if agent.operational_credit < game_launch_cost:
            raise ValidationError("Insufficient operational credit to launch this game.")
            
        try:
            with db_transaction.atomic():
                # 1. Deduct credit from Agent
                agent.operational_credit -= game_launch_cost
                agent.save()

                # 2. Create the GameRound instance
                new_game = serializer.save(
                    agent=agent,
                    game_launch_cost=game_launch_cost,
                    boards_json=generate_boards(total_cards)
                )

                # 3. Create the 'Game Launch Cost' transaction record
                Transaction.objects.create(
                    agent=agent,
                    transaction_type=Transaction.TransactionType.GAME_LAUNCH,
                    amount=game_launch_cost,
                    balance_after_transaction=agent.operational_credit,
                    notes=f"Launch cost for game #{new_game.id}"
                )
        except Exception as e:
            # If anything fails, the atomic transaction rolls back everything
            raise ValidationError(f"An error occurred: {str(e)}")