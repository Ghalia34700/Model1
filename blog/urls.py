from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.user import UserViewSet
from .views import PostViewSet
from .views import CommentViewSet
from .views import CategoryViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns =[
    path('', include(router.urls)),

]
urlpatterns +=router.urls