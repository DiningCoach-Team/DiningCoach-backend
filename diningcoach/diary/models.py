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


class Meal(models.Model):
  MEAL_TYPES = [
    (1, "Breakfast"),
    (2, "Lunch"),
    (3, "Dinner"),
    (4, "Snack")
  ]

  meal_type = models.CharField(verbose_name='식사 종류', max_length=45, choices=MEAL_TYPES)
  content = models.TextField(verbose_name='내용', blank=True, null=True)
  is_deleted = models.BooleanField(verbose_name='삭제 여부', default=False)
  diary = models.ForeignKey(Diary, verbose_name='식단일기', on_delete=models.CASCADE)

  class Meta:
    verbose_name = '식사'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Meal] ' + str(self.diary.date) + ' ' + self.meal_type


class MealImage(models.Model):
  device_id = models.CharField(verbose_name='기기 일련번호', max_length=255, blank=True, null=True)
  image_url = models.TextField(verbose_name='이미지 주소')
  meal = models.ForeignKey(Meal, verbose_name='식사', on_delete=models.CASCADE)

  class Meta:
    verbose_name = '식사 사진'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Meal Image] ' + self.meal
