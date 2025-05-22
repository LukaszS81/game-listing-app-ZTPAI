from .repositories import (
    get_filtered_games,
    get_game_by_id,
    create_game,
    update_game,
    delete_game,
)
from .serializers import GameSerializer, RegisterSerializer

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

from .tasks import notify_game_created

def create_new_game(data):
    serializer = GameSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    game = create_game(validated_data)
    
    # WYWOŁANIE TASKA
    notify_game_created.delay(validated_data['title'])

    return serializer.data
def update_existing_game(game_id, data):
    game = get_game_by_id(game_id)
    serializer = GameSerializer(game, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    update_game(game, validated_data)
    return serializer.data

def delete_existing_game(game_id):
    game = get_game_by_id(game_id)
    delete_game(game)
