from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import (
    Gamer,
    GameObject
)
from .serializers import (
    GamerSerializer,
    GameObjectSerializer
)


class GamerViewSet(ModelViewSet):
    """ViewSet for Gamer."""
    queryset = Gamer.objects.all()
    serializer_class = GamerSerializer
    permission_classes = [IsAuthenticated]


class GameObjectViewSet(ModelViewSet):
    """ViewSet for game object."""
    serializer_class = GameObjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        gamer = Gamer.objects.filter(user=self.request.user.id).first()

        if not gamer:
            return None

        return GameObject.objects.filter(owner=gamer.id)
