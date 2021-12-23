from rest_framework import serializers
from .models import Film

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'poster', 'trailer', 'genre', 'year_released', 'likes', 'dislikes']

class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'poster', 'trailer', 'genre', 'year_released', 'likes', 'dislikes']