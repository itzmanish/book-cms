from django.urls import path, include
from .views import BookApiView, BookDetailView, LoginView, LogoutView
from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token
# from rest_framework.authtoken.views import obtain_auth_token


# router = routers.SimpleRouter()
# router.register(r'', BookViewSet, basename='books')

urlpatterns = [
    # path('login/', obtain_jwt_token, name='login'),
    # path('login/', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    # path('password/reset/', PasswordResetView.as_view()),
    # path('password/change/', PasswordChangeView.as_view()),
    path('', BookApiView.as_view()),
    path('<int:isbn>/', BookDetailView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())

]

# urlpatterns += router.urls
