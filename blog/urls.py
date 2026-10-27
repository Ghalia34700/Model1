from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, get_posts

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns =[
    path( 'posts/get_post/', get_posts, name='get_post'),
]

urlpatterns +=router.urls