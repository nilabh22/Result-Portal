from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FileUpload

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
        validated_data['email'],
        validated_data['password'])

        return user

class FileSerializer(serializers.ModelSerializer):
    """Represents file upload serializer class."""

    class Meta:
        """Contains model & fields used by this serializer."""

        model = FileUpload
        fields = '__all__'
        read_only_fields = ('owner',)