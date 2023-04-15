from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        return {
            "access": data["access"],
            "refresh": data["refresh"],
            "username": self.user.get_username(),
        }


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for create user."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user from db."""
    id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
