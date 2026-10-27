from rest_framework import serializers
from ..models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        #unchangeable fields
        read_only_fields = ('id',)