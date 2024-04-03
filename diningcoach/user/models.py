import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


##### 추상클래스 #####
class TimestampModel(models.Model):
  created_at = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='수정일시', auto_now=True)

  class Meta:
    abstract = True


##### 헬퍼클래스 #####
class UserManager(BaseUserManager):
  use_in_migrations = True

  def create_user(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_superuser', False)

    if not email:
      raise ValueError('User email must be set.')
    email = self.normalize_email(email)

    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    
    return user

  def create_superuser(self, email=None, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self.create_user(email, password, **extra_fields)


##### 회원 #####
class User(AbstractBaseUser, PermissionsMixin):
  PLATFORM_TYPES = [
    ('D', 'DiningCoach'),
    ('K', 'Kakao'),
    ('N', 'Naver'),
    ('G', 'Google'),
    ('A', 'Apple'),
  ]

  id            = models.UUIDField(verbose_name='회원 아이디', primary_key=True, unique=True, editable=False, default=uuid.uuid4)
  username      = models.CharField(verbose_name='사용자명', unique=True, max_length=255, default='user')
  first_name    = None
  last_name     = None
  email         = models.EmailField(verbose_name='이메일', unique=True)
  password      = models.CharField(verbose_name='비밀번호', max_length=255, blank=True, null=True) # When SSO Login, password can be either blank or null
  is_staff      = models.BooleanField(verbose_name='관리페이지 접근가능 여부', default=False)
  is_active     = models.BooleanField(verbose_name='계정활성 여부', default=True)
  is_superuser  = models.BooleanField(verbose_name='모든 권한허용 여부', default=False)
  last_login    = models.DateTimeField(verbose_name='마지막 로그인 일시', auto_now=True)
  date_joined   = models.DateTimeField(verbose_name='계정생성 일시', auto_now_add=True)
  platform_type = models.CharField(verbose_name='가입 플랫폼 종류', max_length=50, blank=True, null=True, choices=PLATFORM_TYPES)
  platform_id   = models.CharField(verbose_name='가입 플랫폼 ID', max_length=255, blank=True, null=True)
  user_agent    = models.TextField(verbose_name='가입 환경 정보', blank=True, null=True)

  objects = UserManager()

  EMAIL_FIELD = 'email'
  USERNAME_FIELD = 'username'

  class Meta:
    db_table = 'user'
    verbose_name = '회원 기본정보'
    verbose_name_plural = verbose_name
    indexes = [
      models.Index(fields=['id'], name='user_id_index'),
      models.Index(fields=['username'], name='user_username_index'),
      models.Index(fields=['email'], name='user_email_index'),
    ]

  def __str__(self):
    return ''.join(
      ['[회원 기본정보] (사용자명 : ', self.username, ', 이메일 : ', self.email, ')']
    )


'''
class User(TimestampModel):
  PLATFORM_TYPES = [
    (0, 'DiningCoach'),
    (1, 'Kakao'),
    (2, 'Naver'),
    (3, 'Google'),
    (4, 'Apple'),
  ]

  id            = models.UUIDField(verbose_name='회원 아이디', primary_key=True, unique=True, editable=False, default=uuid.uuid4)
  email         = models.EmailField(verbose_name='이메일', unique=True)
  password      = models.CharField(verbose_name='비밀번호', max_length=255, blank=True, null=True)
  nickname      = models.CharField(verbose_name='닉네임', max_length=255, default='회원')
  platform_type = models.CharField(verbose_name='가입 플랫폼 종류', max_length=50, blank=True, null=True, choices=PLATFORM_TYPES)
  platform_id   = models.CharField(verbose_name='가입 플랫폼 ID', max_length=255, blank=True, null=True)
  user_agent    = models.TextField(verbose_name='가입 환경 정보')
  is_inactive   = models.BooleanField(verbose_name='휴면회원 여부', default=False)
  is_deleted    = models.BooleanField(verbose_name='삭제 여부', default=False)

  class Meta:
    db_table = 'user'
    verbose_name = '회원'
    verbose_name_plural = verbose_name
    indexes = [
      models.Index(fields=['id'], name='user_id_index'),
      models.Index(fields=['nickname'], name='user_nickname_index'),
      models.Index(fields=['email'], name='user_email_index'),
    ]

  def __str__(self):
    return '회원 : ' + self.email
'''


class UserProfile(TimestampModel):
  GENDER_TYPES = [
    ('M', 'Male'),
    ('F', 'Female'),
  ]

  user              = models.OneToOneField(User, verbose_name='회원', related_name='profile_info', on_delete=models.CASCADE, primary_key=True)
  consent_terms     = models.BooleanField(verbose_name='필수약관 동의 여부', default=False)
  receive_marketing = models.BooleanField(verbose_name='마케팅정보 수신 여부', default=False)
  gender            = models.CharField(verbose_name='성별', max_length=50, blank=True, null=True, choices=GENDER_TYPES)
  birthdate         = models.DateField(verbose_name='생년월일', blank=True, null=True)
  phone_num         = models.CharField(verbose_name='전화번호', max_length=50, blank=True, null=True)
  intro             = models.TextField(verbose_name='자기소개', blank=True, null=True)
  profile_image     = models.TextField(verbose_name='프로필 사진', blank=True, null=True)

  class Meta:
    db_table = 'user_profile'
    verbose_name = '회원 프로필정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return ''.join(
      ['[회원 프로필정보] (사용자명 : ', self.user.username, ', 이메일 : ', self.user.email, ')']
    )


class UserHealth(TimestampModel):
  user            = models.OneToOneField(User, verbose_name='회원', related_name='health_info', on_delete=models.CASCADE, primary_key=True)
  height          = models.IntegerField(verbose_name='키', blank=True, null=True)
  weight          = models.IntegerField(verbose_name='몸무게', blank=True, null=True)
  workout_time    = models.IntegerField(verbose_name='평균 운동량', blank=True, null=True)
  sleep_time      = models.IntegerField(verbose_name='평균 수면시간', blank=True, null=True)
  allergy_info    = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  habit_info      = models.TextField(verbose_name='특이 식습관 정보', blank=True, null=True)
  preference_info = models.TextField(verbose_name='선호 음식 정보', blank=True, null=True)

  class Meta:
    db_table = 'user_health'
    verbose_name = '회원 건강정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return ''.join(
      ['[회원 건강정보] (사용자명 : ', self.user.username, ', 이메일 : ', self.user.email, ')']
    )


'''
class RefreshToken(TimestampModel):
  user          = models.OneToOneField(User, verbose_name='회원', related_name='token_info', on_delete=models.CASCADE, primary_key=True)
  refresh_token = models.CharField(verbose_name='리프레시 토큰', max_length=255)
  is_deleted    = models.BooleanField(verbose_name='삭제 여부', default=False)

  class Meta:
    db_table = 'refresh_token'
    verbose_name = '리프레시 토큰정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return ''.join(
      ['[리프레시 토큰정보] (사용자명 : ', self.user.username, ', 이메일 : ', self.user.email, ')']
    )
'''
