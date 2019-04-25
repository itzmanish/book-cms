from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from rest_framework import viewsets
from django.conf import settings
from .models import Books
from .serializer import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'isbn_10'
    # permission_classes = (IsAuthenticated,)
