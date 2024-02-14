from django.db import models
import uuid


##### 추상클래스 #####
class TimestampModel(models.Model):
  created_at = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='수정일시', auto_now=True)

  class Meta:
    abstract = True


##### 회원 #####
class User(TimestampModel):
  PLATFORM_TYPES = [
    (0, 'DiningCoach'),
    (1, 'Kakao'),
    (2, 'Naver'),
    (3, 'Google'),
    (4, 'Apple'),
  ]

  id            = models.UUIDField(verbose_name='회원 아이디', primary_key=True, unique=True, editable=False, default=uuid.uuid4)
  nickname      = models.CharField(verbose_name='닉네임', max_length=255, unique=True)
  email         = models.EmailField(verbose_name='이메일', unique=True)
  password      = models.CharField(verbose_name='비밀번호', max_length=255, blank=True, null=True)
  platform_type = models.CharField(verbose_name='가입 플랫폼 종류', max_length=50, blank=True, null=True, choices=PLATFORM_TYPES)
  platform_id   = models.CharField(verbose_name='가입 플랫폼 ID', max_length=255, blank=True, null=True)
  user_agent    = models.TextField(verbose_name='가입 환경 정보')
  is_inactive   = models.BooleanField(verbose_name='휴면회원 여부', default=False)
  is_deleted    = models.BooleanField(verbose_name='삭제 여부', default=False)

  class Meta:
    db_table = 'user'
    verbose_name = '회원'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '회원 : ' + self.email


class UserBasic(models.Model):
  GENDER_TYPES = [
    (1, 'Male'),
    (2, 'Female'),
  ]

  user              = models.OneToOneField(User, verbose_name='회원', on_delete=models.CASCADE, primary_key=True)
  consent_terms     = models.BooleanField(verbose_name='필수약관 동의 여부', default=False)
  receive_marketing = models.BooleanField(verbose_name='마케팅정보 수신 여부', default=False)
  gender            = models.CharField(verbose_name='성별', max_length=50, blank=True, null=True, choices=GENDER_TYPES)
  birthdate         = models.DateField(verbose_name='생년월일', blank=True, null=True)
  phone_num         = models.CharField(verbose_name='전화번호', max_length=50, blank=True, null=True)
  intro             = models.TextField(verbose_name='자기소개', blank=True, null=True)
  profile_image     = models.TextField(verbose_name='프로필 사진', blank=True, null=True)

  class Meta:
    db_table = 'user_basic'
    verbose_name = '회원 기본정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '회원 기본정보 : ' + self.user.email


class UserExtra(models.Model):
  user            = models.OneToOneField(User, verbose_name='회원', on_delete=models.CASCADE, primary_key=True)
  height          = models.IntegerField(verbose_name='키', blank=True, null=True)
  weight          = models.IntegerField(verbose_name='몸무게', blank=True, null=True)
  workout_time    = models.IntegerField(verbose_name='평균 운동량', blank=True, null=True)
  sleep_time      = models.IntegerField(verbose_name='평균 수면시간', blank=True, null=True)
  allergy_info    = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  habit_info      = models.TextField(verbose_name='특이 식습관 정보', blank=True, null=True)
  preference_info = models.TextField(verbose_name='선호 음식 정보', blank=True, null=True)

  class Meta:
    db_table = 'user_extra'
    verbose_name = '회원 추가정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '회원 추가정보 : ' + self.user.email


class RefreshToken(TimestampModel):
  user          = models.OneToOneField(User, verbose_name='회원', on_delete=models.CASCADE, primary_key=True)
  refresh_token = models.CharField(verbose_name='리프레시 토큰', max_length=255)
  is_deleted    = models.BooleanField(verbose_name='삭제 여부', default=False)

  class Meta:
    db_table = 'refresh_token'
    verbose_name = '리프레시 토큰'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '리프레시 토큰 : ' + self.user.email
