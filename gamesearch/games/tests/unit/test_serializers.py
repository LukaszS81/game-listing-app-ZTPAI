from django.test import TestCase
from games.serializers import GameSerializer

class GameSerializerTestCase(TestCase):
    def test_game_serializer_valid_data(self):
        data = {
            "title": "Valid Game",
            "genre": "Action",
            "description": "A cool action game",
            "img": "http://example.com/valid.png"
        }
        serializer = GameSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

    def test_game_serializer_invalid_data(self):
        data = {
            "title": "",  # Title is required
            "genre": "Action"
        }
        serializer = GameSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_missing_required_fields(self):
        serializer = GameSerializer(data={})
        self.assertFalse(serializer.is_valid())
        # wymagane są title i genre
        self.assertEqual(set(serializer.errors.keys()), {"title", "genre"})

    def test_allows_missing_optional_fields(self):
        data = {
            "title": "Minimal",
            "genre": "Arcade"
            # description i img nie są przekazane
        }
        serializer = GameSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        validated = serializer.validated_data
        self.assertEqual(validated["title"], "Minimal")
        self.assertEqual(validated["genre"], "Arcade")
        self.assertNotIn("description", validated)
        self.assertNotIn("img", validated)

    def test_title_and_genre_max_length(self):
        # test max_length validation for title and genre
        data = {
            "title": "x" * 201,    # max_length=200
            "genre": "y" * 101     # max_length=100
        }
        serializer = GameSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("genre", serializer.errors)
