from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных модели User."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class OwnerSerializer(serializers.ModelSerializer):
    """Сериализация данных модели User для своей учётной записи."""

    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализация данных при регистрации."""

    class Meta:
        fields = ('email', 'username')
        model = User


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
