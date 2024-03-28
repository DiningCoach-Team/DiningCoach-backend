from django.contrib.auth import authenticate
import re

from user.models import User, UserProfile

from rest_framework import serializers


class UserSignUpSerializer(serializers.Serializer):
  username = serializers.CharField(required=True, max_length=255)
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, max_length=255)
  user_agent = serializers.CharField(required=True)

  def validate_email(self, value):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, value):
      raise serializers.ValidationError('이메일 형식이 올바르지 않습니다.')
    elif User.objects.filter(email=value).exists():
      raise serializers.ValidationError('해당 이메일로 등록된 계정이 이미 존재합니다.')
    return value

  # Password must have
  # 1) minimum 8 characters and maximum 16 characters in length. -> {8,16}
  # 2) at least one uppercase alphabet. -> (?=.*?[A-Z])
  # 3) at least one lowercase alphabet. -> (?=.*?[a-z])
  # 4) at least one digit. -> (?=.*?[0-9])
  # 5) at least one special character. -> (?=.*?[#?!@$%^&*-])
  def validate_password(self, value):
    password_format = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).$'
    if not re.match(password_format, value):
      raise serializers.ValidationError('비밀번호는 소문자, 대문자, 숫자, 특수문자를 각각 최소 1개 이상 포함하도록 설정해주세요.')
    elif len(value) < 8:
      raise serializers.ValidationError('비밀번호는 8자리 이상으로 설정해주세요.')
    elif len(value) > 16:
      raise serializers.ValidationError('비밀번호는 16자리 이하로 설정해주세요.')
    return value

  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password'],
      platform_type=(0, 'DiningCoach'),
      platform_id=None,
      user_agent=validated_data['user_agent'],
    )

    return user


class UserLoginSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, max_length=255)

  def validate(self, data):
    # Validate email
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, data['email']):
      raise serializers.ValidationError('이메일 형식이 올바르지 않습니다.')
    elif not User.objects.filter(email=data['email']).exists():
      raise serializers.ValidationError('해당 이메일로 등록된 계정이 존재하지 않습니다.')

    # Authenticate user
    user = authenticate(email=data['email'], password=data['password'])
    if user is None:
      raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')

    return data


class UserBaseRetrieveSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    exclude = ['password']


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
  profile_user = UserBaseRetrieveSerializer(many=False, read_only=True)

  class Meta:
    model = UserProfile
    fields = '__all__'
