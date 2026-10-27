from rest_framework import serializers
from ..models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        #unchangeable fields
        read_only_fields = ('id',)