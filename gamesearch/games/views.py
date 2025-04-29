from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .services import (
    register_user,
    list_all_games,
    get_game_details,
    create_new_game,
    update_existing_game,
    delete_existing_game,
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse

def custom_404_handler(request, exception):
    return JsonResponse({
        "error": "Not Found",
        "status": 404
    }, status=404)

def custom_500_handler(request):
    return JsonResponse({
        "error": "Internal Server Error",
        "status": 500
    }, status=500)

@swagger_auto_schema(
    method='post',
    operation_description="Rejestracja nowego użytkownika.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    user_data = register_user(request.data)
    return Response(user_data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get',
    operation_description="Lista wszystkich gier z opcjonalnym filtrowaniem po tytule i gatunku.",
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Tytuł gry", type=openapi.TYPE_STRING),
        openapi.Parameter('genre', openapi.IN_QUERY, description="Gatunek gry", type=openapi.TYPE_STRING),
    ],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def list_games(request):
    title = request.query_params.get('title', '')
    genre = request.query_params.get('genre', '')
    games = list_all_games(title, genre)
    return Response(games, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_description="Szczegóły gry na podstawie ID.",
)
@api_view(['GET'])
@permission_classes([AllowAny])
def game_detail(request, game_id):
    game = get_game_details(game_id)
    return Response(game, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_description="Dodanie nowej gry (wymaga uwierzytelnienia).",
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_game(request):
    game = create_new_game(request.data)
    return Response(game, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='patch',
    operation_description="Aktualizacja danych gry (wymaga uwierzytelnienia).",
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_game(request, game_id):
    game = update_existing_game(game_id, request.data)
    return Response(game, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='delete',
    operation_description="Usunięcie gry (wymaga uwierzytelnienia).",
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_game(request, game_id):
    delete_existing_game(game_id)
    return Response(status=status.HTTP_204_NO_CONTENT)
