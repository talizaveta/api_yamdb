from django.utils import timezone

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError

from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка методов GET, POST, PUT, PATCH, DELETE  для произведений."""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')

    def perform_create(self, serializer):
        if self.kwargs.get('year') > timezone.now().year:
            raise ValidationError('Год выхода еще не существует!')
        serializer.save()


class CategoryViewSet(ListCreateDestroyViewSet):
    """Обработка методов GET, POST, DELETE для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )


class GenreViewSet(ListCreateDestroyViewSet):
    """Обработка методов GET, POST, DELETE для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
