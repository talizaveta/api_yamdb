from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Comment, Review, Title
from users.models import User
from .permissions import AdminOnly, ReviewAndCommentPermission
from .serializers import (
    CommentSerializer, GetTokenSerializer, OwnerSerializer,
    ReviewSerializer, SignUpSerializer, UserSerializer)


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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'], detail=False,
        url_path='me', permission_classes=(IsAuthenticated,))
    def get_patch_owner_info(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = OwnerSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = OwnerSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
     def post(self, request):
         serializer = SignUpSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         try:
             user, create = User.objects.get_or_create(
                 **serializer.validated_data
             )
         except IntegrityError:
             return Response('Имя пользователя или почта уже существуют!',
                             status=status.HTTP_400_BAD_REQUEST)
         confirmation_code = default_token_generator.make_token(user)
         user.confirmation_code = confirmation_code
         user.save()
         send_mail(
             subject='Yamdb confirmation code',
             message=f'Ваш код подтверждения: {confirmation_code}',
             from_email=DEFAULT_FROM_EMAIL,
             recipient_list=[user.email],
         )
         return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )
        if default_token_generator.check_token(
                user, serializer.validated_data.get('confirmation_code')
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
