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
                {"error": "Invalid page or limit."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start = (page - 1) * limit
        end = start + limit

        categories = Category.objects.all()[start:end]
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

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )