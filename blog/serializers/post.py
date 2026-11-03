from rest_framework import serializers
from ..models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author','categories']
        #unchangeable fields
        read_only_fields = ('id',)
