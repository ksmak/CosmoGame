from rest_framework import serializers

from .models import (
    Gamer,
    GameObject
)


class GamerSerializer(serializers.ModelSerializer):
    """Serializer for gamer."""
    props = serializers.JSONField(required=False)

    class Meta:
        model = Gamer
        fields = (
            'id',
            'user',
            'avatar',
            'props'
        )


class GameObjectSerializer(serializers.ModelSerializer):
    """Serializer for game object."""
    props = serializers.JSONField(required=False)

    class Meta:
        model = GameObject
        fields = (
            'id',
            'state',
            'obj_type',
            'order_number',
            'name',
            'owner',
            'coords',
            'level',
            'props',
            'expired_date'
        )
