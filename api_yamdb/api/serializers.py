from rest_framework import serializers

from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Title."""

    rating = serializers.DecimalField(
        read_only=True,
        max_digits=2,
        decimal_places=1
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'description',
            'year',
            'rating',
            'genre',
            'category',
        )


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

