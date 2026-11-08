from rest_framework import serializers
from ..models import Category

class CategorySerializer(serializers.ModelSerializer):
    '''
    name = serializers.CharField(
        read_only=True,
        allow_blank=False,
        max_length=100,
    )
    '''
    class Meta:
        model = Category
        fields = ['id', 'name', 'description','created_at']
        #unchangeable fields
        read_only_fields = ['id', 'created_at']