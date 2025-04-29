# urls.py
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('games/', views.list_games, name='list_games'),                         # GET: lista gier + filtrowanie
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),          # GET: szczegóły jednej gry
    path('games/create/', views.create_game, name='create_game'),                 # POST: dodanie gry
    path('games/<int:game_id>/update/', views.update_game, name='update_game'),   # PATCH: edycja gry
    path('games/<int:game_id>/delete/', views.delete_game, name='delete_game'),   # DELETE: usunięcie gry
    path('register/', views.register, name='register'),                          # POST: rejestracja użytkownika
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # odśwież token
]
