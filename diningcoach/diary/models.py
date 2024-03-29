from django.db import models
from user.models import User


##### 추상클래스 #####
class TimestampModel(models.Model):
  created_at = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
  updated_at = models.DateTimeField(verbose_name='수정일시', auto_now=True)

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


##### 식단일기 #####
class MealDiary(TimestampModel):
  MEAL_TYPES = [
    (1, 'Breakfast'),
    (2, 'Lunch'),
    (3, 'Dinner'),
    (4, 'Snack'),
  ]

  date         = models.DateField(verbose_name='식단일기 날짜')
  meal_type    = models.CharField(verbose_name='식사 종류', max_length=50, choices=MEAL_TYPES)
  content      = models.TextField(verbose_name='내용', blank=True, null=True)
  is_favourite = models.BooleanField(verbose_name='즐겨찾기', default=False)
  is_public    = models.BooleanField(verbose_name='공개 여부', default=False)
  is_deleted   = models.BooleanField(verbose_name='삭제 여부', default=False)
  user         = models.ForeignKey(User, verbose_name='회원', on_delete=models.CASCADE)

  class Meta:
    db_table = 'meal_diary'
    verbose_name = '식사일기'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '식사일기 : ' + str(self.date) + ' ' + self.meal_type


class MealImage(TimestampModel):
  image_url   = models.TextField(verbose_name='이미지 주소')
  device_info = models.TextField(verbose_name='기기 정보', blank=True, null=True)
  is_deleted  = models.BooleanField(verbose_name='삭제 여부', default=False)
  meal        = models.ForeignKey(MealDiary, verbose_name='식사일기', on_delete=models.CASCADE)

  class Meta:
    db_table = 'meal_image'
    verbose_name = '식사 사진'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '식사 사진 : ' + str(self.meal.date) + ' ' + self.meal.meal_type


class MealFood(models.Model):
  FOOD_TYPES = [
    (1, 'Processed Food'),
    (2, 'Fresh Food'),
    (3, 'Cooked Food'),
  ]

  food_code = models.CharField(verbose_name='식품코드', max_length=50)
  food_name = models.CharField(verbose_name='식품명', max_length=255)
  food_type = models.CharField(verbose_name='식품 종류', max_length=50, choices=FOOD_TYPES)
  portion   = models.FloatField(verbose_name='비율', blank=True, null=True, default=1.0)
  meal      = models.ForeignKey(MealDiary, verbose_name='식사일기', on_delete=models.CASCADE)

  class Meta:
    db_table = 'meal_food'
    verbose_name = '식사 음식'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '식사 음식 : ' + str(self.meal.date) + ' ' + self.meal.meal_type


class MealNutrition(NutritionModel):
  meal = models.OneToOneField(MealDiary, verbose_name='식사일기', on_delete=models.CASCADE, primary_key=True)

  class Meta:
    db_table = 'meal_nutrition'
    verbose_name = '식사 영양정보'
    verbose_name_plural = verbose_name

  def __str__(self):
    return '식사 영양정보 : ' + str(self.meal.date) + ' ' + self.meal.meal_type
