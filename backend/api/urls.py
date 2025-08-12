# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AgentDetailView, TransactionListView, GameOptionsView, GameRoundCreateView

urlpatterns = [
    # Auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Agent
    path('me/', AgentDetailView.as_view(), name='agent-detail'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    
    # Game
    path('game-options/', GameOptionsView.as_view(), name='game-options'),
    path('game-rounds/', GameRoundCreateView.as_view(), name='game-round-create'),
]