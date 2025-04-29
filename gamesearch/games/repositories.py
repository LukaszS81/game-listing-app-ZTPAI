from .models import Game
from django.shortcuts import get_object_or_404

def get_filtered_games(title='', genre=''):
    return Game.objects.filter(
        title__icontains=title,
        genre__icontains=genre
    )

def get_game_by_id(game_id):
    return get_object_or_404(Game, id=game_id)

def create_game(validated_data):
    return Game.objects.create(**validated_data)

def update_game(game, validated_data):
    for attr, value in validated_data.items():
        setattr(game, attr, value)
    game.save()
    return game

def delete_game(game):
    game.delete()
