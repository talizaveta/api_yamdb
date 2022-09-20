from reviews.models import Category, Comment, Genre, Review, Title
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            request.method != 'PATCH'
                and Review.objects.filter(
                title=title,
                author=request.user).exists()
        ):
            raise serializers.ValidationError('Отзыв уже создан!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
