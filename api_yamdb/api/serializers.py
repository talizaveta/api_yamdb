from reviews.models import Category, Genre, Title
from rest_framework import serializers


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Title."""

    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'rating', 'genre', 'category',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация данных модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)

