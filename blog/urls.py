from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.generate import generate_post
from .views.user import UserViewSet
from .views import PostViewSet
from .views import CommentViewSet
from .views import CategoryViewSet

from .view import summarize_post_view


router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns =[
    path('', include(router.urls)),
    path('posts/generate/', generate_post, name='generate_post'),
    path("posts/<int:post_id>/summarize/",summarize_post_view,
         name="summarize-post"
         ),

]
urlpatterns +=router.urls