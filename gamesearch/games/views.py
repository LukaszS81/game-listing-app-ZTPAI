# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Game
from .serializers import GameSerializer
from django.db.models import Q
from .serializers import RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Lista wszystkich gier + możliwość filtrowania po tytule i gatunku
@api_view(['GET'])
@permission_classes([AllowAny])
def list_games(request):
    title = request.query_params.get('title', '')
    genre = request.query_params.get('genre', '')
    games = Game.objects.filter(
        Q(title__icontains=title) & Q(genre__icontains=genre)
    )
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 🔹 Szczegóły gry po ID
@api_view(['GET'])
@permission_classes([AllowAny])
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    serializer = GameSerializer(game)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 🔹 Dodanie nowej gry
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_game(request):
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Aktualizacja gry
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    serializer = GameSerializer(game, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔹 Usunięcie gry
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
