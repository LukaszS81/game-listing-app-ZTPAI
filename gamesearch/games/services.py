from .repositories import (
    get_filtered_games,
    get_game_by_id,
    create_game,  # create_game z repositories.py – zapis do bazy
    update_game,
    delete_game,
)
from .serializers import GameSerializer, RegisterSerializer
from .tasks import notify_game_created

def register_user(data):
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

def list_all_games(title='', genre=''):
    games = get_filtered_games(title, genre)
    return GameSerializer(games, many=True).data

def get_game_details(game_id):
    game = get_game_by_id(game_id)
    return GameSerializer(game).data

def create_new_game(data, request=None):
    serializer = GameSerializer(data=data, context={'request': request})  # dodaj request do context!
    serializer.is_valid(raise_exception=True)
    game = serializer.save()  # w create() user będzie wzięty z request
    notify_game_created.delay(game.title)
    return GameSerializer(game).data


def update_existing_game(game_id, data):
    game = get_game_by_id(game_id)
    serializer = GameSerializer(game, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data

def delete_existing_game(game_id):
    game = get_game_by_id(game_id)
    delete_game(game)
