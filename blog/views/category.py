from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import CategorySerializer
from ..models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['GET'])
def get_categories(request):
    try:
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))

        if page < 1 or limit < 1 or limit > 100:
            return Response(
                {"error": "Page must be at least 1 and limit must be between 1 and 100."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start = (page - 1) * limit
        end = start + limit

        categories = Category.objects.all().order_by('id')[start:end]
        serializer = CategorySerializer(categories, many=True)

        return Response({
            'categories': serializer.data,
            'page': page,
            'limit': limit,
            'start': start,
        })

    except (ValueError, TypeError):
        return Response(
            {"error": "Page and limit must be integers."},
            status=status.HTTP_400_BAD_REQUEST
        )