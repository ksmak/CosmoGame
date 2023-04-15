from django.contrib.auth import get_user_model

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    MyTokenObtainPairSerializer,
    UserCreateSerializer,
)


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request: Request) -> Response:
    serializer: UserCreateSerializer
    serializer = UserCreateSerializer(
        data=request.data
    )

    if not serializer.is_valid():
        return Response({
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    user: User = serializer.save()

    return Response({
        "result": "OK",
        "activation_code": user.activation_code
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request: Request, activation_code: str) -> Response:
    user = User.objects.filter(activation_code=activation_code).first()

    if not user:
        return Response({
            "error": "User not found."
        }, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save(update_fields=('is_active', ))

    return Response({
        "result": "OK",
        }, status=status.HTTP_200_OK
    )
