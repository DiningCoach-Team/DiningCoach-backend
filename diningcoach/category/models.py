from django.db import models


class FoodCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    verbose_name = '식품분류 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Food Category] ' + self.category_name


class PreferenceCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    verbose_name = '선호음식 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Preference Category] ' + self.category_name


class AllergyCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    verbose_name = '알레르기 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Allergy Category]' + self.category_name


class HabitCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    verbose_name = '식습관 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Habit Category] ' + self.category_name
