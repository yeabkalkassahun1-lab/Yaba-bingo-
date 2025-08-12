# games/models.py
from django.db import models
from accounts.models import Agent

class GameSpeed(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # Example: 1.0 for normal, 0.7 for fast, 1.5 for slow
    speed_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)

    def __str__(self):
        return self.name

class WinningPattern(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Stores a 5x5 grid, e.g., [[1,1,1,1,1], [0,0,0,0,0], ...] where 1 is a required square
    pattern_json = models.JSONField()

    def __str__(self):
        return self.name

class GameRound(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='game_rounds')
    game_speed = models.ForeignKey(GameSpeed, on_delete=models.PROTECT)
    winning_pattern = models.ForeignKey(WinningPattern, on_delete=models.PROTECT)
    
    card_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cards = models.IntegerField(default=100)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    game_launch_cost = models.DecimalField(max_digits=10, decimal_places=2)
    boards_json = models.JSONField() # Stores the set of 100 generated boards
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game by {self.agent.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"