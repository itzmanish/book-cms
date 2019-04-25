from rest_framework_jwt.settings import api_settings
from .utils import jwt_blacklist, jwt_is_blacklisted
from rest_framework_jwt.compat import Serializer
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta
import jwt
from rest_framework import serializers
from .models import Books

# Serializers define the API representation.


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = "isbn_10"
        model = Books
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    pass


class LogoutSerializer(serializers.ModelSerializer):
    pass
