from django.db import models
from user.models import User


#################### 식품 ####################
class CustomizedFood(models.Model):
  food_type = models.CharField(verbose_name='식품 종류', max_length=45)
  food_category = models.CharField(verbose_name='식품 분류', max_length=255, blank=True, null=True)
  name = models.CharField(verbose_name='식품명', max_length=255)
  brand_name = models.CharField(verbose_name='제조사명', max_length=255, blank=True, null=True)
  barcode = models.IntegerField(verbose_name='유통바코드', blank=True, null=True)
  amount_per_serving = models.IntegerField(verbose_name='1회제공량', blank=True, null=True)
  created_at = models.DateTimeField(verbose_name='생성 일시', auto_now_add=True)
  user = models.ForeignKey(User, verbose_name='회원', on_delete=models.CASCADE)

  class Meta:
    verbose_name = '사용자 추가식품'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Customized Food] ' + self.name


class ProcessedFood(models.Model):
  food_image = models.TextField(verbose_name='식품 사진', blank=True, null=True)
  food_category = models.CharField(verbose_name='식품 분류', max_length=255)
  name = models.CharField(verbose_name='식품명', max_length=255)
  country = models.CharField(verbose_name='제조국', max_length=255, blank=True, null=True)
  brand_name = models.CharField(verbose_name='제조사명', max_length=255, blank=True, null=True)
  report_no = models.IntegerField(verbose_name='품목보고번호', blank=True, null=True)
  food_kind = models.CharField(verbose_name='식품유형', max_length=255, blank=True, null=True)
  allergy_info = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  storage = models.TextField(verbose_name='보관방법', blank=True, null=True)
  barcode = models.IntegerField(verbose_name='유통바코드', blank=True, null=True)
  amount_per_serving = models.IntegerField(verbose_name='1회제공량', blank=True, null=True)

  class Meta:
    verbose_name = '가공식품'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Processed Food] ' + self.name


class FreshFood(models.Model):
  food_image = models.TextField(verbose_name='식품 사진', blank=True, null=True)
  food_category = models.CharField(verbose_name='식품 분류', max_length=255)
  name = models.CharField(verbose_name='식품명', max_length=255)
  country = models.CharField(verbose_name='제조국', max_length=255, blank=True, null=True)
  brand_name = models.CharField(verbose_name='제조사명', max_length=255, blank=True, null=True)
  report_no = models.IntegerField(verbose_name='품목보고번호', blank=True, null=True)
  food_kind = models.CharField(verbose_name='식품유형', max_length=255, blank=True, null=True)
  allergy_info = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  storage = models.TextField(verbose_name='보관방법', blank=True, null=True)
  barcode = models.IntegerField(verbose_name='유통바코드', blank=True, null=True)
  amount_per_serving = models.IntegerField(verbose_name='1회제공량', blank=True, null=True)

  class Meta:
    verbose_name = '신선식품'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Fresh Food] ' + self.name
