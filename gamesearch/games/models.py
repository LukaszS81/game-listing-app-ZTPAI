from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    img = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
