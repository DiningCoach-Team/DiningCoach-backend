from django.db import models
import uuid


class User(models.Model):
  PLATFORM_TYPES = [
    (1, "Kakao"),
    (2, "Google"),
    (3, "Apple")
  ]

  id = models.UUIDField(verbose_name='', primary_key=True, unique=True, editable=False, default=uuid.uuid4)
  email = models.EmailField(verbose_name='이메일', unique=True)
  password = models.CharField(verbose_name='비밀번호', max_length=255, blank=True, null=True)
  platform_type = models.CharField(verbose_name='가입 플랫폼 종류', max_length=45, blank=True, null=True, choices=PLATFORM_TYPES)
  platform_id = models.CharField(verbose_name='가입 플랫폼 ID', max_length=255, blank=True, null=True)
  user_agent = models.TextField(verbose_name='가입 환경 정보')
  created_at = models.DateTimeField(verbose_name='가입 일시', auto_now_add=True)
  modified_at = models.DateTimeField(verbose_name='수정 일시', auto_now=True)
  is_deleted = models.BooleanField(verbose_name='삭제 여부', default=False)

  class Meta:
    verbose_name = '회원'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[User] ' + self.email


class UserBasic(models.Model):
  GENDER_TYPES = [
    (1, "Male"),
    (2, "Female")
  ]

  user = models.OneToOneField(User, verbose_name='회원', on_delete=models.CASCADE, primary_key=True)
  nickname = models.CharField(verbose_name='닉네임', max_length=255, blank=True, null=True)
  consent_terms = models.BooleanField(verbose_name='필수약관 동의 여부', default=False)
  receive_marketing = models.BooleanField(verbose_name='마케팅정보 수신 여부', default=False)
  gender = models.CharField(verbose_name='성별', max_length=45, blank=True, null=True, choices=GENDER_TYPES)
  birthdate = models.DateField(verbose_name='생년월일', blank=True, null=True)
  phone_num = models.CharField(verbose_name='전화번호', max_length=45, blank=True, null=True)
  intro = models.TextField(verbose_name='자기소개', blank=True, null=True)
  profile_image = models.TextField(verbose_name='프로필 사진', blank=True, null=True)

  class Meta:
    verbose_name = '회원 기본정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[User Basic Info] ' + self.user
