from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication

from .serializers import RegistrationSerializer, UserLoginSerializer, UserProfileSerializer



User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            Token.objects.create(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            users = User.objects.filter(email=serializer.validated_data['email'])
            if users.exists():
                user = users.first()
                if user.check_password(serializer.validated_data['password']):
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    return Response({'msg': 'неверный пароль'}, status=400)
            return Response({'msg': 'пользователь не найден'}, status=400)
        return Response(serializer.errors, status=400)

            
        
        
class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
