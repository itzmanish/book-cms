from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .authentication import ExpiringTokenAuthentication

from rest_framework.permissions import IsAuthenticated
from .models import Book, ExpiringToken
from .serializer import BookSerializer, LoginSerializer


class BookApiView(APIView):
    '''
    BookApiView Class based view returns list of books.
    '''

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request) -> 'Response':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=200)

    def post(self, request) -> 'Response':
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookDetailView(APIView):
    '''
    It return detail view of a specific book.
    '''

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, isbn) -> 'Queryset':
        try:
            return Book.objects.get(isbn_10=isbn)
        except Book.DoesNotExist as e:
            return None
        # This is same as :
        # return get_object_or_404(Books, isbn_10=isbn)

    def get(self, request, isbn=None):
        instance = self.get_object(isbn)
        if instance is not None:
            serializer = BookSerializer(instance)
            return Response(serializer.data)
        return Response({'errors': 'The book you are looking for does not exist.'}, status=404)

    def patch(self, request, isbn=None):
        data = request.data
        instance = self.get_object(isbn)
        if instance is not None:
            serializer = BookSerializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({'errors': 'The book you are looking for does not exist.'}, status=404)

    def delete(self, isbn=None):
        instance = self.get_object(isbn)
        instance.delete()
        return HttpResponse('Book item has been deleted successfully', status=204)


class LoginView(APIView):

    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = ExpiringToken.objects.get_or_create(user=user)
        if token.expired():
            # If the token is expired, generate a new one.
            token.delete()
            token = ExpiringToken.objects.create(
                user=user
            )
        return Response({'key': token.key}, status=200)


class LogoutView(APIView):

    authentication_classes = [ExpiringTokenAuthentication, ]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        django_logout(request)
        return Response('Successfully logged out.', status=204)
