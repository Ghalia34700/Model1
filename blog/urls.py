from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.user import UserViewSet
from .views import PostViewSet, get_posts
from .views import CommentViewSet, get_comments
from .views import CategoryViewSet, get_categories

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('users', UserViewSet, basename='users')
#router.register('comments', CommentViewSet)
#router.register('categories', CategoryViewSet)

urlpatterns =[
    path('posts/get_post/', get_posts, name='get_posts'),
    path('', include(router.urls)),
   # path('comment/get_comments/', get_comments, name='get_comment'),
    #path('catategory/get_categories/', get_categories, name='get_categories'),

]
urlpatterns +=router.urls