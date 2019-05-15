from rest_framework import serializers

from forge.models import World


class WorldSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = World
        fields = [
            'name',
            'genre',
            'description',
            'story',
            'creator',
        ]
        read_only_fields = ['id']