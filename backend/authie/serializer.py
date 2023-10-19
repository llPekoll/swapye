from rest_framework import serializers

from .models import GameDefaults, MailingInfo, Reset, UserAccount, UserPersonalInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("email", "password")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=200)


class UserPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalInfo
        exclude = ("owner",)


class MailingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingInfo
        exclude = ("owner",)


class GameDefaultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameDefaults
        exclude = ("owner",)
