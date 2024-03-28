import re
from user.models import User
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

  def validate_email(self, value):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, value):
      raise serializers.ValidationError('이메일 형식이 올바르지 않습니다.')
    return value
