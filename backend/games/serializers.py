from rest_framework import serializers

from .models import Game, Lead, Price, WinnedPrice


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        # fields = ['id', 'account_name', 'users', 'created']

    def create(self, validated_data):
        return Game(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.content = validated_data.get("content", instance.content)
        instance.created = validated_data.get("created", instance.created)
        return instance
