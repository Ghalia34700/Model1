from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import PostSerializer
from ..models import Post

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(['GET'])
def get_posts(request):
    try:
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))

        if page < 1 or limit < 1 or limit > 100:
            return Response(
                {"error": "Invalid page or limit."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start = (page - 1) * limit
        end = start + limit

        posts = Post.objects.all()[start:end]
        serializer = PostSerializer(posts, many=True)

        return Response({
            'posts': serializer.data,
            'page': page,
            'limit': limit,
            'start': start
        })

    except (ValueError, TypeError):
        return Response(
            {"error": "Page and limit must be integers."},
            status=status.HTTP_400_BAD_REQUEST
        )