from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse

# Zadania Celery
from games.tasks import sample_task, notify_game_created

# Logika biznesowa
from .services import (
    register_user,
    list_all_games,
    get_game_details,
    create_new_game,
    update_existing_game,
    delete_existing_game,
)

# Własne strony błędów
def custom_404_handler(request, exception):
    return JsonResponse({"error": "Not Found", "status": 404}, status=404)

def custom_500_handler(request):
    return JsonResponse({"error": "Internal Server Error", "status": 500}, status=500)

# Rejestracja użytkownika z zadaniem Celery
@swagger_auto_schema(
    method='post',
    operation_description="Rejestracja nowego użytkownika.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    user_data = register_user(request.data)
    sample_task.delay(f"Nowy użytkownik zarejestrowany: {user_data['username']}")
    return Response(user_data, status=status.HTTP_201_CREATED)

# Lista gier (dla użytkownika)
@swagger_auto_schema(
    method='get',
    operation_description="Lista wszystkich gier z opcjonalnym filtrowaniem po tytule i gatunku.",
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Tytuł gry", type=openapi.TYPE_STRING),
        openapi.Parameter('genre', openapi.IN_QUERY, description="Gatunek gry", type=openapi.TYPE_STRING),
    ],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_games(request):
    title = request.query_params.get('title', '')
    genre = request.query_params.get('genre', '')
    games = list_all_games(title, genre)
    return Response(games, status=status.HTTP_200_OK)

# Szczegóły gry
@swagger_auto_schema(
    method='get',
    operation_description="Szczegóły gry na podstawie ID.",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_detail(request, game_id):
    game = get_game_details(game_id)
    return Response(game, status=status.HTTP_200_OK)

# Dodawanie gry + kolejka Celery
@swagger_auto_schema(
    method='post',
    operation_description="Dodanie nowej gry (wymaga uprawnień administratora).",
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_game(request):
    game = create_new_game(request.data)
    notify_game_created.apply_async(args=[game['title']], queue='game-tasks')
    return Response(game, status=status.HTTP_201_CREATED)

# Edycja gry
@swagger_auto_schema(
    method='patch',
    operation_description="Aktualizacja danych gry (wymaga uprawnień administratora).",
)
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_game(request, game_id):
    game = update_existing_game(game_id, request.data)
    return Response(game, status=status.HTTP_200_OK)

# Usuwanie gry
@swagger_auto_schema(
    method='delete',
    operation_description="Usunięcie gry (wymaga uprawnień administratora).",
)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_game(request, game_id):
    delete_existing_game(game_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
