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
