from django.db import models


##### 카테고리 #####
class FoodCategory(models.Model):
  category_name   = models.CharField(verbose_name='카테고리명', max_length=255)
  depth           = models.IntegerField(verbose_name='카테고리 계층', default=0)
  parent_category = models.ForeignKey('self', verbose_name='상위 카테고리', on_delete=models.CASCADE, blank=True, null=True)

  class Meta:
    db_table = 'food_category'
    verbose_name = '식품분류 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '식품분류 카테고리 : ' + self.category_name + ' (계층 : ' + str(self.depth) + ')'


class HabitCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)
  habit_type = models.CharField(verbose_name='식습관 종류', max_length=50)

  class Meta:
    db_table = 'habit_category'
    verbose_name = '식습관 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '식습관 카테고리 : ' + self.category_name


class PreferenceCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    db_table = 'preference_category'
    verbose_name = '선호음식 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '선호음식 카테고리 : ' + self.category_name


class AllergyCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    db_table = 'allergy_category'
    verbose_name = '알레르기 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '알레르기 카테고리 : ' + self.category_name
