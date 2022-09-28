import re
from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404

from reviews.models import Categories, Comment, Genres, Review, Title
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Categories."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Genres."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Title."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                {'year': f'Год не может быть больше {current_year}'}
            )
        return value


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Title."""

    genre = GenresSerializer(many=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        title = self.context['request'].parser_context['kwargs']['title_id']
        request = self.context.get('request')
        if (
            request.method != 'PATCH'
                and Review.objects.filter(
                title=title,
                author=request.user).exists()
        ):
            raise serializers.ValidationError('Вы уже оставляли рецензию.')
        return data

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация данных модели Comment."""

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

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    """Сериализация данных при регистрации."""

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать <me> в качестве никнейма'
            )
        elif re.search(r'^[\w.@+-]+$', value) is None:
            raise serializers.ValidationError(
                'Использованы недопустимые символы'
            )
        return value


class GetTokenSerializer(serializers.Serializer):
    """Сериализация данных при получении токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
