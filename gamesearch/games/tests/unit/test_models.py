from django.test import TestCase
from django.core.exceptions import ValidationError
from games.models import Game

class GameModelTestCase(TestCase):
    def test_create_game(self):
        game = Game.objects.create(
            title="Test Game",
            genre="Adventure",
            description="Test description",
            img="http://example.com/test-image.png"
        )
        self.assertEqual(game.title, "Test Game")
        self.assertEqual(game.genre, "Adventure")
        self.assertEqual(game.description, "Test description")
        self.assertEqual(game.img, "http://example.com/test-image.png")

    def test_create_game_without_optional_fields(self):
        # description i img mogą być None
        game = Game.objects.create(title="Minimal", genre="Arcade")
        self.assertIsNone(game.description)
        self.assertIsNone(game.img)

    def test_str_method(self):
        # __str__ powinno zwracać title
        game = Game.objects.create(title="Title", genre="G")
        self.assertEqual(str(game), "Title")

    def test_title_max_length(self):
        # tytuł dłuższy niż 200 znaków powinien walidować się błędem
        game = Game(title="x" * 201, genre="G")
        with self.assertRaises(ValidationError):
            game.full_clean()

    def test_genre_max_length(self):
        # gatunek dłuższy niż 100 znaków powinien walidować się błędem
        game = Game(title="T", genre="x" * 101)
        with self.assertRaises(ValidationError):
            game.full_clean()

    def test_missing_required_fields(self):
        # brak title i genre powinien rzucić ValidationError
        game = Game(description="D", img="http://example.com")
        with self.assertRaises(ValidationError):
            game.full_clean()

    def test_optional_fields_allow_blank(self):
        # description i img mogą być puste stringi
        game = Game(title="T", genre="G", description="", img="")
        # full_clean() nie powinno rzucić błędu
        game.full_clean()

    def test_img_url_invalid(self):
        # niepoprawny format URL w img powinien rzucić ValidationError
        game = Game(title="T", genre="G", img="not-a-url")
        with self.assertRaises(ValidationError):
            game.full_clean()
