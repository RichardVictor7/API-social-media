from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    """Serializer específico para operações de like"""
    class Meta:
        model = Post
        fields = ['id', 'liked']
    
    def update(self, instance, validated_data):
        """Toggle do status de like"""
        instance.liked = not instance.liked  # Inverte o status atual
        instance.save()
        return instance