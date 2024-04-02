from user.models import User, UserProfile, UserHealth

from rest_framework import serializers


class AuthUserKakaoSerializer(serializers.Serializer):
  pass


class AuthUserGoogleSerializer(serializers.Serializer):
  pass


class AuthUserAppleSerializer(serializers.Serializer):
  pass


class AuthUserNaverSerializer(serializers.Serializer):
  pass
