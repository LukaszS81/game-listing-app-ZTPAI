from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import notify_game_created


class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    img = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')

    def __str__(self):
        return self.title


# Sygnał uruchamiający zadanie Celery po utworzeniu gry
@receiver(post_save, sender=Game)
def game_created_handler(sender, instance, created, **kwargs):
    if created:
        notify_game_created.delay(instance.title)
