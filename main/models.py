from django.db import models

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=200)
    poster = models.CharField(max_length=200)
    trailer = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    year_released = models.IntegerField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
