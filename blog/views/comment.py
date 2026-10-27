from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import CommentSerializer
from ..models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['GET'])
def get_comments(request):
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

        comments = Comment.objects.all()[start:end]
        serializer = CommentSerializer(comments, many=True)

        return Response({
            'comments': serializer.data,
            'page': page,
            'limit': limit,
            'start': start,
        })

    except (ValueError, TypeError):
        return Response(
            {"error": "Page and limit must be integers."},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )