from rest_framework import serializers
from .models import User

# Class to serialize the response
class UserSerializer(serializers.ModelSerializer):
    # "Meta" class it manage the data convertion of the object db (ORM)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    # Method of UserSerializer that creates a new element
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)