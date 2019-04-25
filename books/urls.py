from django.urls import path, include
from .views import BookViewSet
from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework.authtoken.views import obtain_auth_token

app_name = 'books'

router = routers.SimpleRouter()
router.register(r'', BookViewSet)

urlpatterns = [
    # path('login/', obtain_jwt_token, name='login'),
    # path('login/', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    # path('password/reset/', PasswordResetView.as_view()),
    # path('password/change/', PasswordChangeView.as_view()),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt'))
]

urlpatterns += router.urls
