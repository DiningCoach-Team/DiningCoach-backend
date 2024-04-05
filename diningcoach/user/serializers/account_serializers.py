import re

from user.models import User, UserProfile, UserHealth
from user.exceptions import *

from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserSignUpSerializer(serializers.Serializer):
  # This serializer is not used
  pass

  '''
  PLATFORM_TYPE = 'D'
  PLATFORM_ID = None

  username = serializers.CharField(required=True, max_length=255)
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, max_length=255)
  # user_agent = serializers.CharField(required=True)

  def validate_username(self, value):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(email_format, value):
      raise InvalidUsernameFormatException(detail=('INVALID_USERNAME', '이름(사용자명)은 이메일 형식이 될 수 없습니다.'))
    elif User.objects.filter(username=value).exists():
      raise AccountAlreadyExistsException(detail=('ACCOUNT_ALREADY_EXISTS', '해당 이름(사용자명)으로 등록된 계정이 이미 존재합니다.'))
    return value

  def validate_email(self, value):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, value):
      raise InvalidEmailFormatException(detail=('INVALID_EMAIL', '이메일 입력 형식이 올바르지 않습니다.'))
    elif User.objects.filter(email=value).exists():
      raise AccountAlreadyExistsException(detail=('ACCOUNT_ALREADY_EXISTS', '해당 이메일로 등록된 계정이 이미 존재합니다.'))
    return value

  # Password must have
  # 1) minimum 8 characters and maximum 16 characters in length. -> {8,16}
  # 2) at least one uppercase alphabet. -> (?=.*?[A-Z])
  # 3) at least one lowercase alphabet. -> (?=.*?[a-z])
  # 4) at least one digit. -> (?=.*?[0-9])
  # 5) at least one special character. -> (?=.*?[#?!@$%^&*-])
  def validate_password(self, value):
    password_format = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{,}$'
    if not re.match(password_format, value):
      raise InvalidPasswordFormatException(detail=('INVALID_PASSWORD', '비밀번호는 소문자, 대문자, 숫자, 특수문자를 각각 최소 1개 이상 포함하도록 설정해주세요.'))
    elif len(value) < 8:
      raise InvalidPasswordFormatException(detail=('INVALID_PASSWORD', '비밀번호는 8자리 이상으로 설정해주세요.'))
    elif len(value) > 16:
      raise InvalidPasswordFormatException(detail=('INVALID_PASSWORD', '비밀번호는 16자리 이하로 설정해주세요.'))
    return value

  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password'],
      platform_type=self.PLATFORM_TYPE,
      platform_id=self.PLATFORM_ID,
      user_agent=self.context.META['HTTP_USER_AGENT'],
    )

    return user
  '''


class UserLoginSerializer(serializers.Serializer):
  # This serializer is not used
  pass

  '''
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True, max_length=255)

  def validate(self, data):
    # Validate email
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, data['email']):
      raise InvalidEmailFormatException(detail=('INVALID_EMAIL', '이메일 입력 형식이 올바르지 않습니다.'))
    elif not User.objects.filter(email=data['email']).exists():
      raise AccountNotExistsException(detail=('ACCOUNT_NOT_EXISTS', '해당 이메일로 등록된 계정이 존재하지 않습니다.'))

    # Authenticate user
    user = authenticate(email=data['email'], password=data['password'])
    if user is None:
      raise AuthenticationFailedException(detail=('AUTHENTICATION_FAILED', '비밀번호가 일치하지 않습니다.'))

    return data
  '''


class AccountSignUpSerializer(RegisterSerializer):
  PLATFORM_TYPE = 'D'
  PLATFORM_ID = None

  def validate_username(self, value):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(email_format, value):
      raise InvalidUsernameFormatException(detail=('INVALID_USERNAME', '이름(사용자명)은 이메일 형식이 될 수 없습니다.'))
    elif User.objects.filter(username=value).exists():
      raise AccountAlreadyExistsException(detail=('ACCOUNT_ALREADY_EXISTS', '해당 이름(사용자명)으로 등록된 계정이 이미 존재합니다.'))
    return value

  def validate_email(self, value):
    email_format = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.match(email_format, value):
      raise InvalidEmailFormatException(detail=('INVALID_EMAIL', '이메일 입력 형식이 올바르지 않습니다.'))
    elif User.objects.filter(email=value).exists():
      raise AccountAlreadyExistsException(detail=('ACCOUNT_ALREADY_EXISTS', '해당 이메일로 등록된 계정이 이미 존재합니다.'))
    return value
  
  # Password must have
  # 1) minimum 8 characters and maximum 16 characters in length. -> {8,16}
  # 2) at least one uppercase alphabet. -> (?=.*?[A-Z])
  # 3) at least one lowercase alphabet. -> (?=.*?[a-z])
  # 4) at least one digit. -> (?=.*?[0-9])
  # 5) at least one special character. -> (?=.*?[#?!@$%^&*-])
  def validate_password1(self, value):
    password_format = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{,}$'
    if not re.match(password_format, value):
      raise InvalidPasswordFormatException(detail=('INVALID_PASSWORD', '비밀번호는 소문자, 대문자, 숫자, 특수문자를 각각 최소 1개 이상 포함하도록 설정해주세요.'))
    elif len(value) < 8:
      raise InvalidPasswordFormatException(detail=('INVALID_PASSWORD', '비밀번호는 8자리 이상으로 설정해주세요.'))
    elif len(value) > 16:
      raise InvalidPasswordFormatException(detail=('INVALID_PASSWORD', '비밀번호는 16자리 이하로 설정해주세요.'))
    return value

  def save(self, request):
    user = super().save(request)

    try:
      user_id = getattr(user, 'id')
    except AttributeError:
      raise CreateDataFailedException(detail=('CREATE_DATA_FAILED', '회원 데이터는 성공적으로 생성되었으나, 프로필 데이터와 건강 데이터 생성에는 실패하였습니다.'))

    user_profile = UserProfile.objects.create(
      user_id=user_id,
      consent_terms=False,
      receive_marketing=False,
    )
    user_profile.save()

    user_health = UserHealth.objects.create(
      user_id=user_id,
    )
    user_health.save()

    return user


class AccountPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
  uid = None
  token = None

  def validate(self, attrs):
    uid = self.context['view'].kwargs['uidb64']
    token = self.context['view'].kwargs['token']

    attrs['uid'] = uid
    attrs['token'] = token

    return super().validate(attrs)
