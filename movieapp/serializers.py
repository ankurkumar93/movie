from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class MovieDetailsSerializer(serializers.Serializer):
    
    title = serializers.CharField(max_length=128)
    genre = serializers.CharField(max_length=128)
    description = serializers.CharField()


class AddCollectionSerializer(serializers.Serializer):

    title = serializers.CharField(max_length=128)
    description = serializers.CharField()
    movies = serializers.ListField(child=MovieDetailsSerializer())

        