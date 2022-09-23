from django.utils import timezone
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination, ValidationError
from reviews.models import Comment, Review, Title, Category, Genre

from api.mixins import ListCreateDestroyViewSet
from .permissions import ReviewAndCommentPermission, IsAdminOrReadOnly
from .serializer import (CommentSerializer, ReviewSerializer, CategorySerializer,
                         GenreSerializer, TitleSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewAndCommentPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(
                title=title_id,
                author=self.request.user
        ).exists():
            raise ParseError('Отзыв уже создан!')
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewAndCommentPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
    

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
