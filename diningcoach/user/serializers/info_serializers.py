import re

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
  def validate_username(self, value):
    if self.context['request'].user.username == value:
      return value
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(email_format, value):
      raise InvalidUsernameFormatException(detail=('INVALID_USERNAME', '이름(사용자명)은 이메일 형식이 될 수 없습니다.'))
    elif User.objects.filter(username=value).exists():
      raise AccountAlreadyExistsException(detail=('ACCOUNT_ALREADY_EXISTS', '해당 이름(사용자명)으로 등록된 계정이 이미 존재합니다.'))
    return value

  def validate_email(self, value):
    if self.context['request'].user.email == value:
      return value
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, value):
      raise InvalidEmailFormatException(detail=('INVALID_EMAIL', '이메일 입력 형식이 올바르지 않습니다.'))
    elif User.objects.filter(email=value).exists():
      raise AccountAlreadyExistsException(detail=('ACCOUNT_ALREADY_EXISTS', '해당 이메일로 등록된 계정이 이미 존재합니다.'))
    return value

  def validate_is_active(self, value):
    if not self.context['request'].user.is_active and not value:
      raise UpdateNotAllowedException(detail=('UPDATE_NOT_ALLOWED', '계정이 비활성화되어 있어 정보를 변경할 수 없습니다.'))
    return value


class UserProfileUpdateSerializer(UserProfileDefaultSerializer):
  def validate(self, data):
    if not self.context['request'].user.is_active:
      raise UpdateNotAllowedException(detail=('UPDATE_NOT_ALLOWED', '계정이 비활성화되어 있어 정보를 변경할 수 없습니다.'))
    return data

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
  def validate(self, data):
    if not self.context['request'].user.is_active:
      raise UpdateNotAllowedException(detail=('UPDATE_NOT_ALLOWED', '계정이 비활성화되어 있어 정보를 변경할 수 없습니다.'))
    return data

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
