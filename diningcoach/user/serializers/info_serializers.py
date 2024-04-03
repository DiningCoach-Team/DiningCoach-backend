from user.models import User, UserProfile, UserHealth
from user.exceptions import *

from rest_framework import serializers


##### Default Serializer #####
class UserBasicDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'is_active', 'platform_type', 'platform_id']


class UserProfileDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    exclude = ['user', 'created_at', 'updated_at']
    # extra_kwargs = {
    #   'user': {'validators': []},
    # }


class UserHealthDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserHealth
    exclude = ['user', 'created_at', 'updated_at']
    # extra_kwargs = {
    #   'user': {'validators': []},
    # }


##### Retrieve Serializer #####
class UserBasicRetrieveSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password']


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'

  def to_representation(self, instance):
    ret = super().to_representation(instance)
    ret['user'] = UserBasicRetrieveSerializer(instance=instance.user).data
    return ret

  '''
  profile_info = UserProfileDefaultSerializer(many=False, read_only=True)

  class Meta(UserBasicDefaultSerializer.Meta):
    pass
  '''


class UserHealthRetrieveSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserHealth
    fields = '__all__'

  def to_representation(self, instance):
    ret = super().to_representation(instance)
    ret['user'] = UserBasicRetrieveSerializer(instance=instance.user).data
    return ret

  '''
  health_info = UserHealthDefaultSerializer(many=False, read_only=True)

  class Meta(UserBasicDefaultSerializer.Meta):
    pass
  '''


##### Update Serializer #####
class UserBasicUpdateSerializer(UserBasicDefaultSerializer):
  pass


class UserProfileUpdateSerializer(UserProfileDefaultSerializer):
  pass

  '''
  profile_info = UserProfileDefaultSerializer(many=False, read_only=False)

  class Meta(UserBasicDefaultSerializer.Meta):
    pass

  def update(self, instance, validated_data):
    profile_serializer = self.fields['profile_info']
    profile_instance = instance.profile_info
    profile_validated_data = validated_data.pop('profile_info')

    profile_serializer.update(profile_instance, profile_validated_data)
    return super().update(instance, validated_data)
  '''


class UserHealthUpdateSerializer(UserHealthDefaultSerializer):
  pass

  '''
  health_info = UserHealthDefaultSerializer(many=False, read_only=False)

  class Meta(UserBasicDefaultSerializer.Meta):
    pass

  def update(self, instance, validated_data):
    health_serializer = self.fields['health_info']
    health_instance = instance.health_info
    health_validated_data = validated_data.pop('health_info')

    health_serializer.update(health_instance, health_validated_data)
    return super().update(instance, validated_data)
  '''
