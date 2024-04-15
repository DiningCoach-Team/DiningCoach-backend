import os
from django.db import models
from user.models import User


##### 이미지 업로드 주소 #####
def food_image_path(instance, filename):
  food_type = instance.Meta.db_table
  food_code = instance.food_code
  return os.path.join('food', food_type, food_code, filename)


##### 추상클래스 #####
class FoodModel(models.Model):
  food_code      = models.CharField(verbose_name='식품코드', max_length=50, unique=True)
  food_name      = models.CharField(verbose_name='식품명', max_length=255)
  country_origin = models.CharField(verbose_name='제조국가', max_length=50, blank=True, null=True)
  manufacturer   = models.CharField(verbose_name='지역/제조사', max_length=255, blank=True, null=True)
  category_main  = models.CharField(verbose_name='식품대분류', max_length=50)
  category_sub   = models.CharField(verbose_name='식품상세분류', max_length=50)
  food_image     = models.ImageField(verbose_name='식품 이미지', upload_to=food_image_path, blank=True, null=True)
  allergy_info   = models.TextField(verbose_name='알레르기 정보', blank=True, null=True)
  storage_info   = models.TextField(verbose_name='보관방법 정보', blank=True, null=True)

  class Meta:
    abstract = True


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


##### 식품 #####
class CustomizedFood(FoodModel):
  user = models.ForeignKey(User, verbose_name='회원', on_delete=models.CASCADE)

  class Meta:
    db_table = 'customized_food'
    verbose_name = '사용자 추가식품'
    verbose_name_plural = verbose_name
    indexes = [
      models.Index(fields=['food_code'], name='customized_food_code_index'),
      models.Index(fields=['food_name'], name='customized_food_name_index'),
      models.Index(fields=['category_main', 'category_sub'], name='customized_food_category_index'),
    ]

  def __str__(self):
    return '사용자 추가식품 : ' + self.food_name


class CustomizedMetadata(TimestampModel):
  FOOD_TYPES = [
    ('P', 'Processed Food'),
    ('F', 'Fresh Food'),
    ('C', 'Cooked Food'),
  ]

  customized_food = models.OneToOneField(CustomizedFood, verbose_name='사용자 추가식품', on_delete=models.CASCADE, primary_key=True)
  food_type       = models.CharField(verbose_name='식품 종류', max_length=50, choices=FOOD_TYPES)
  additional_info = models.TextField(verbose_name='추가정보', blank=True, null=True)
  is_deleted      = models.BooleanField(verbose_name='삭제 여부', default=False)

  class Meta:
    db_table = 'customized_metadata'
    verbose_name = '사용자 추가식품 메타데이터'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '사용자 추가식품 메타데이터 : ' + self.customized_food.food_name


class ProcessedFood(FoodModel):
  barcode_no = models.CharField(verbose_name='유통바코드', max_length=50)

  class Meta:
    db_table = 'processed_food'
    verbose_name = '가공식품'
    verbose_name_plural = verbose_name
    indexes = [
      models.Index(fields=['food_code'], name='processed_food_code_index'),
      models.Index(fields=['food_name'], name='processed_food_name_index'),
      models.Index(fields=['category_main', 'category_sub'], name='processed_food_category_index'),
      models.Index(fields=['barcode_no'], name='processed_food_barcode_index'),
    ]

  def __str__(self):
    return '가공식품 : ' + self.food_name


class FreshFood(FoodModel):
  harvest_time = models.CharField(verbose_name='채취시기', max_length=50)

  class Meta:
    db_table = 'fresh_food'
    verbose_name = '신선식품'
    verbose_name_plural = verbose_name
    indexes = [
      models.Index(fields=['food_code'], name='fresh_food_code_index'),
      models.Index(fields=['food_name'], name='fresh_food_name_index'),
      models.Index(fields=['category_main', 'category_sub'], name='fresh_food_category_index'),
    ]

  def __str__(self):
    return '신선식품 : ' + self.food_name


class CookedFood(FoodModel):
  product_type = models.CharField(verbose_name='상용제품', max_length=50)

  class Meta:
    db_table = 'cooked_food'
    verbose_name = '조리식품'
    verbose_name_plural = verbose_name
    indexes = [
      models.Index(fields=['food_code'], name='cooked_food_code_index'),
      models.Index(fields=['food_name'], name='cooked_food_name_index'),
      models.Index(fields=['category_main', 'category_sub'], name='cooked_food_category_index'),
    ]

  def __str__(self):
    return '조리식품 : ' + self.food_name


##### 영양성분 #####
class CustomizedNutrition(NutritionModel):
  customized_food = models.OneToOneField(CustomizedFood, verbose_name='사용자 추가식품', related_name='nutrition_info', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    db_table = 'customized_nutrition'
    verbose_name = '사용자 추가식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '사용자 추가식품 영양정보 : ' + self.customized_food.food_name


class ProcessedNutrition(NutritionModel):
  processed_food = models.OneToOneField(ProcessedFood, verbose_name='가공식품', related_name='nutrition_info', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    db_table = 'processed_nutrition'
    verbose_name = '가공식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '가공식품 영양정보 : ' + self.processed_food.food_name


class FreshNutrition(NutritionModel):
  fresh_food = models.OneToOneField(FreshFood, verbose_name='신선식품', related_name='nutrition_info', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    db_table = 'fresh_nutrition'
    verbose_name = '신선식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '신선식품 영양정보 : ' + self.fresh_food.food_name


class CookedNutrition(NutritionModel):
  cooked_food = models.OneToOneField(CookedFood, verbose_name='조리식품', related_name='nutrition_info', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    db_table = 'cooked_nutrition'
    verbose_name = '조리식품 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '조리식품 영양정보 : ' + self.cooked_food.food_name
