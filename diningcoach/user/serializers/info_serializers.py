from user.models import User, UserProfile, UserHealth
from user.exceptions import *

from rest_framework import serializers


class UserDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password', 'is_staff', 'is_superuser', 'groups', 'user_permissions']


class UserProfileDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'


class UserHealthDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserHealth
    fields = '__all__'


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
  profile_info = UserProfileDefaultSerializer(many=False, read_only=True)

  class Meta(UserDefaultSerializer.Meta):
    pass


class UserHealthRetrieveSerializer(serializers.ModelSerializer):
  health_info = UserHealthDefaultSerializer(many=False, read_only=True)

  class Meta(UserDefaultSerializer.Meta):
    pass
