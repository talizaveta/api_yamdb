from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Comment, Review, Title

from .permissions import ReviewAndCommentPermission
from .serializers import (CommentSerializer, ReviewSerializer,)


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


class UsersViewSet():
    pass
