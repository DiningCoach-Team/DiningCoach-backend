from django.db import models
from user.models import User


class Diary(models.Model):
  date = models.DateField(verbose_name='날짜')
  is_deleted = models.BooleanField(verbose_name='삭제 여부', default=False)
  user = models.ForeignKey(User, verbose_name='회원', on_delete=models.CASCADE)

  class Meta:
    verbose_name = '식단일기'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Diary] ' + str(self.date)
