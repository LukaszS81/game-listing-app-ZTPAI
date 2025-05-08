from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    img = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    def __str__(self):
        return self.title
