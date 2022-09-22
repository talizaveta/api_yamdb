from django.urls import include, path
from rest_framework import routers

from .views import (
    CommentViewSet, ReviewsViewSet, UsersViewSet,
    GetTokenView, SignUpView)

app_name = 'api'

v1_router = routers.DefaultRouter()


v1_review = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet
)
v1_comment = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/auth/signup/', SignUpView.as_view())
]
