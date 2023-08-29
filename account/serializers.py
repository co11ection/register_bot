from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'full_name', 'phone_number')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Set and hash the password
        user.save()
        return user
        


from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password, request=self.context.get('request'))

            if not user:
                raise serializers.ValidationError('Пользователь не найден')
            
            data['user'] = user
        else:
            raise serializers.ValidationError('Email и пароль обязательны')

        return data



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'phone_number')