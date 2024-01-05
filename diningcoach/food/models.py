from django.db import models
from user.models import User


#################### 추상클래스 ####################
class FoodModel(models.Model):
  food_code      = models.CharField(verbose_name='식품코드', max_length=50, unique=True)
  food_name      = models.CharField(verbose_name='식품명', max_length=255)
  country_origin = models.CharField(verbose_name='제조국가', max_length=50, blank=True, null=True)
  manufacturer   = models.CharField(verbose_name='지역/제조사', max_length=50, blank=True, null=True)
  category_main  = models.CharField(verbose_name='식품대분류', max_length=50)
  category_sub   = models.CharField(verbose_name='식품상세분류', max_length=50)
  food_image     = models.TextField(verbose_name='식품 이미지', blank=True, null=True)
  allergy_info   = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  storage_info   = models.TextField(verbose_name='보관방법 정보', blank=True, null=True)

  class Meta:
    abstract = True
    indexes = [
      models.Index(fields=['food_code'], name='%(class)s_code_index'),
      models.Index(fields=['food_name'], name='%(class)s_name_index'),
      models.Index(fields=['category_main', 'category_sub'], name='%(class)s_category_index'),
    ]


class NutritionModel(models.Model):
  amount_per_serving = models.FloatField(verbose_name='1회제공량(g)', blank=True, null=True, default=0.0)
  calorie            = models.FloatField(verbose_name='칼로리(kcal)', blank=True, null=True, default=0.0)
  carbohydrate       = models.FloatField(verbose_name='탄수화물(g)', blank=True, null=True, default=0.0)
  sugar              = models.FloatField(verbose_name='당류(g)', blank=True, null=True, default=0.0)
  protein            = models.FloatField(verbose_name='단백질(g)', blank=True, null=True, default=0.0)
  fat                = models.FloatField(verbose_name='지방(g)', blank=True, null=True, default=0.0)
  cholesterol        = models.FloatField(verbose_name='콜레스테롤(mg)', blank=True, null=True, default=0.0)
  sodium             = models.FloatField(verbose_name='나트륨(mg)', blank=True, null=True, default=0.0)
  saturated_fat      = models.FloatField(verbose_name='포화지방(g)', blank=True, null=True, default=0.0)
  trans_fat          = models.FloatField(verbose_name='트랜스지방(g)', blank=True, null=True, default=0.0)

  class Meta:
    abstract = True


class TimestampModel(models.Model):
  created_at = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='수정일시', auto_now=True)

  class Meta:
    abstract = True


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


class CookedFood(models.Model):
  food_image = models.TextField(verbose_name='식품 사진', blank=True, null=True)
  food_category = models.CharField(verbose_name='식품 분류', max_length=255, blank=True, null=True)
  name = models.CharField(verbose_name='식품명', max_length=255)
  food_kind = models.CharField(verbose_name='식품유형', max_length=255, blank=True, null=True)
  allergy_info = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  storage = models.TextField(verbose_name='보관방법', blank=True, null=True)
  amount_per_serving = models.IntegerField(verbose_name='1회제공량', blank=True, null=True)

  class Meta:
    verbose_name = '조리식품'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Cooked Food] ' + self.name


#################### 영양성분 ####################
class NutritionInfo(models.Model):
  calorie = models.IntegerField(verbose_name='칼로리(kcal)', blank=True, null=True, default=0)
  carbohydrate = models.IntegerField(verbose_name='탄수화물(g)', blank=True, null=True, default=0)
  sugar = models.IntegerField(verbose_name='당류(g)', blank=True, null=True, default=0)
  protein = models.IntegerField(verbose_name='단백질(g)', blank=True, null=True, default=0)
  fat = models.IntegerField(verbose_name='지방(g)', blank=True, null=True, default=0)
  cholesterol = models.IntegerField(verbose_name='콜레스테롤(mg)', blank=True, null=True, default=0)
  sodium = models.IntegerField(verbose_name='나트륨(mg)', blank=True, null=True, default=0)
  saturated_fat = models.IntegerField(verbose_name='포화지방(g)', blank=True, null=True, default=0)
  trans_fat = models.IntegerField(verbose_name='트랜스지방(g)', blank=True, null=True, default=0)

  class Meta:
    abstract = True


class CustomizedNutrition(NutritionInfo):
  food = models.OneToOneField(CustomizedFood, verbose_name='추가식품', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    verbose_name = '사용자 추가식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Customized Food Nutrition] ' + self.food.name


class ProcessedNutrition(NutritionInfo):
  food = models.OneToOneField(ProcessedFood, verbose_name='가공식품', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    verbose_name = '가공식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Processed Food Nutrition] ' + self.food.name


class FreshNutrition(NutritionInfo):
  food = models.OneToOneField(FreshFood, verbose_name='신선식품', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    verbose_name = '신선식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Fresh Food Nutrition] ' + self.food.name


class CookedNutrition(NutritionInfo):
  food = models.OneToOneField(CookedFood, verbose_name='조리식품', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    verbose_name = '조리식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '[Cooked Food Nutrition] ' + self.food.name
