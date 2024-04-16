import os
import datetime

from django.utils import timezone
from django.db import transaction, IntegrityError
from django.conf import settings

from food.models import ProcessedFood, FreshFood, CookedFood
from diary.models import MealDiary, MealFood, MealNutrition
from diary.exceptions import CreateDataFailedException, UpdateDataFailedException, DeleteDataFailedException

from rest_framework import serializers

from celery import shared_task


class MealNutritionDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealNutrition
    fields = '__all__'


def generate_meal_nutrition(meal_food_list, meal_diary_id):
  meal_nutrition_dict = {
    'amount_per_serving': 0.0,
    'calorie': 0.0,
    'carbohydrate': 0.0,
    'sugar': 0.0,
    'protein': 0.0,
    'fat': 0.0,
    'cholesterol': 0.0,
    'sodium': 0.0,
    'saturated_fat': 0.0,
    'trans_fat': 0.0,
  }

  if meal_food_list.exists():
    meal_food_list = list(meal_food_list)
  else:
    meal_nutrition_dict['meal'] = meal_diary_id
    return meal_nutrition_dict

  for meal_food in meal_food_list:
    food_code = meal_food.food_code
    food_type = meal_food.food_type
    portion = meal_food.portion

    food_instance = None

    if food_type == 'P':
      food_instance = ProcessedFood.objects.filter(
        food_code__exact=food_code
      ).prefetch_related('nutrition_info')
    elif food_type == 'F':
      food_instance = FreshFood.objects.filter(
        food_code__exact=food_code
      ).prefetch_related('nutrition_info')
    elif food_type == 'C':
      food_instance = CookedFood.objects.filter(
        food_code__exact=food_code
      ).prefetch_related('nutrition_info')
    else:
      meal_nutrition_dict['meal'] = meal_diary_id
      return meal_nutrition_dict

    if food_instance is not None and food_instance.exists():
      nutrition_instance = food_instance.get().nutrition_info
    else:
      meal_nutrition_dict['meal'] = meal_diary_id
      return meal_nutrition_dict

    for key, value in meal_nutrition_dict.items():
      meal_nutrition_dict[key] = value + (getattr(nutrition_instance, key) * portion)

  meal_nutrition_dict['meal'] = meal_diary_id
  return meal_nutrition_dict


@shared_task(bind=False)
@transaction.atomic
def write_meal_nutrition(meal_diary_id):
  try:
    meal_food_list = MealFood.objects.select_for_update().filter(
      meal_id__exact=meal_diary_id
    )

    meal_nutrition_data = generate_meal_nutrition(meal_food_list, meal_diary_id)

    meal_nutrition_serializer = MealNutritionDefaultSerializer(data=meal_nutrition_data)
    meal_nutrition_serializer.is_valid(raise_exception=True)
    meal_nutrition_serializer.save()
  except IntegrityError:
    raise CreateDataFailedException(detail=('CREATE_DATA_FAILED', '식단일기 영양성분 데이터 생성에 실패하였습니다.'))


@shared_task(bind=False)
@transaction.atomic
def edit_meal_nutrition(meal_diary_id):
  try:
    meal_food_list = MealFood.objects.select_for_update().filter(
      meal_id__exact=meal_diary_id
    )

    meal_nutrition_data = generate_meal_nutrition(meal_food_list, meal_diary_id)
    meal_nutrition_instance = MealNutrition.objects.select_for_update().filter(
      meal_id__exact=meal_diary_id
    )
    if meal_nutrition_instance.exists():
      meal_nutrition_instance = meal_nutrition_instance.get()
    else:
      meal_nutrition_instance = None

    meal_nutrition_serializer = MealNutritionDefaultSerializer(instance=meal_nutrition_instance, data=meal_nutrition_data)
    meal_nutrition_serializer.is_valid(raise_exception=True)
    meal_nutrition_serializer.save()
  except IntegrityError:
    raise UpdateDataFailedException(detail=('UPDATE_DATA_FAILED', '식단일기 영양성분 데이터 수정에 실패하였습니다.'))


def delete_meal_image(meal_image_list):
  if meal_image_list is None or not meal_image_list.exists():
    return

  meal_image_list = list(meal_image_list)
  for meal_image_instance in meal_image_list:
    image_file_path = os.path.join(settings.MEDIA_ROOT, str(meal_image_instance.image_url))
    if os.path.exists(image_file_path):
      os.remove(image_file_path)

    meal_image_instance.delete()


def delete_meal_food(meal_food_list):
  if meal_food_list is None or not meal_food_list.exists():
    return

  meal_food_list = list(meal_food_list)
  for meal_food_instance in meal_food_list:
    meal_food_instance.delete()


def delete_meal_nutrition(meal_nutrition_instance):
  if meal_nutrition_instance is None:
    return

  meal_nutrition_instance.delete()


@transaction.atomic
def delete_meal_diary():
  current_time = timezone.now()
  thirty_days = datetime.timedelta(days=30)

  try:
    meal_diary_list = MealDiary.objects.select_for_update().filter(
      is_deleted__exact=True,
      updated_at__lt=(current_time - thirty_days),
    ).prefetch_related(
      'meal_image',
      'meal_food',
      'meal_nutrition',
    )

    if not meal_diary_list.exists():
      return

    meal_diary_list = list(meal_diary_list)
    for meal_diary in meal_diary_list:
      if hasattr(meal_diary, 'meal_image'):
        delete_meal_image(meal_diary.meal_image.all())
      if hasattr(meal_diary, 'meal_food'):
        delete_meal_food(meal_diary.meal_food.all())
      if hasattr(meal_diary, 'meal_nutrition'):
        delete_meal_nutrition(meal_diary.meal_nutrition)

      meal_diary.delete()
  except IntegrityError:
    raise DeleteDataFailedException(detail=('DELETE_DATA_FAILED', '식단일기 데이터 영구 삭제에 실패하였습니다.'))
