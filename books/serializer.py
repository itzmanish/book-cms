from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from .models import Book

# Serializers define the API representation.


class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Book
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'User is disabled.'
                    raise exceptions.ValidationError(msg)
            else:
                msg = 'Authentication failed'
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide and username both'
            raise exceptions.ValidationError(msg)
        return data


class LogoutSerializer(serializers.ModelSerializer):
    pass
