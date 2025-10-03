from rest_framework import serializers
from ..models import Room, Category, Status

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'created_at']

class RoomSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), allow_null=True)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'price', 'photo', 'category', 'status']