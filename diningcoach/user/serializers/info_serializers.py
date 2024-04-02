from user.models import User, UserProfile, UserHealth
from user.exceptions import *

from rest_framework import serializers


class _UserBasicDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password', 'is_staff', 'is_superuser', 'groups', 'user_permissions']


class _UserProfileDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'


class _UserHealthDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserHealth
    fields = '__all__'


class UserBasicRetrieveSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password']


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
  profile_info = _UserProfileDefaultSerializer(many=False, read_only=True)

  class Meta(_UserBasicDefaultSerializer.Meta):
    pass


class UserHealthRetrieveSerializer(serializers.ModelSerializer):
  health_info =_UserHealthDefaultSerializer(many=False, read_only=True)

  class Meta(_UserBasicDefaultSerializer.Meta):
    pass
