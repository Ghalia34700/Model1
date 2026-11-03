from rest_framework import serializers
from ..models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'author', 'post']
        #unchangeable fields
        read_only_fields = ('id',)