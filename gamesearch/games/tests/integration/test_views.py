from django.test import TestCase

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from games.models import Game

class GameAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.game = Game.objects.create(title="Test Game", genre="Action", description="Test Desc", img="http://example.com/image.png")

    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "password": "newpass123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_games(self):
        url = reverse('list_games')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_game_detail(self):
        url = reverse('game_detail', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.game.title)

    def test_create_game_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('create_game')
        data = {
            "title": "New Game",
            "genre": "Adventure",
            "description": "A new adventure game.",
            "img": "http://example.com/newimage.png"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_game_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('update_game', args=[self.game.id])
        data = {
            "description": "Updated description"
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Updated description")

    def test_delete_game_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('delete_game', args=[self.game.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_game_detail_not_found(self):
        url = reverse('game_detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['status'], status.HTTP_404_NOT_FOUND)

    def test_create_game_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('create_game')
        payload = {"genre": "Puzzle"}  # brak title
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # teraz błędy walidacji są w response.data['error']
        self.assertIn('title', response.data['error'])
        # oraz możesz dodatkowo sprawdzić treść:
        self.assertEqual(
            response.data['error']['title'][0].code,
            'required'
        )

    def test_delete_game_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('delete_game', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

