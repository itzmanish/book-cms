from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Book(models.Model):

    book = models.CharField(max_length=100)
    image = models.ImageField(upload_to="book_image/", blank=True, null=True)
    description = models.TextField()
    isbn_10 = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=20)
    binding = models.CharField(max_length=20)
    no_of_pages = models.IntegerField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.book


class ExpiringToken(Token):

    """Extend Token to add an expired method."""

    class Meta(object):
        proxy = True

    def expired(self):
        """Return boolean indicating token expiration."""
        now = timezone.now()
        if self.created < now - settings.TOKEN_EXPIRE_TIME:
            return True
        return False
