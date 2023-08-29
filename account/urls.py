from django.urls import path, include
from .views import RegistrationView, UserLoginView, UserProfileView
urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
]