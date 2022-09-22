from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()

v1_router.register(r'genre/', GenreViewSet)
v1_router.register(r'category/', CategoryViewSet)
v1_router.register(r'title/', TitleViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
