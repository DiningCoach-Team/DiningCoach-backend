from django.db import models


class FoodCategory(models.Model):
  category_name = models.CharField(verbose_name='카테고리명', max_length=255)

  class Meta:
    verbose_name = '식품분류 카테고리'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Food Category] ' + self.category_name
