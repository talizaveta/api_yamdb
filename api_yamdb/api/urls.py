from django.urls import include, path
from rest_framework import routers
from .views import (CommentViewSet, ReviewsViewSet, CategoryViewSet,
                    GenreViewSet, TitleViewSet)

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

app_name = 'api'

v1_router.register(r'genre/', GenreViewSet)
v1_router.register(r'category/', CategoryViewSet)
v1_router.register(r'title/', TitleViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
