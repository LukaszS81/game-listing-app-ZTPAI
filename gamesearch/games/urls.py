# urls.py
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('games/', views.list_games),                         # GET: lista gier + filtrowanie
    path('games/<int:game_id>/', views.game_detail),          # GET: szczegóły jednej gry
    path('games/create/', views.create_game),                 # POST: dodanie gry
    path('games/<int:game_id>/update/', views.update_game),   # PATCH: edycja gry
    path('games/<int:game_id>/delete/', views.delete_game),   # DELETE: usunięcie gry
    path('register/', views.register),                        # POST: rejestracja użytkownika
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # odśwież token
]
