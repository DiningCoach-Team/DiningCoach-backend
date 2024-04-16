from django.db import transaction, IntegrityError

from food.models import ProcessedFood, FreshFood, CookedFood
from diary.models import MealFood, MealNutrition
from diary.exceptions import CreateDataFailedException, UpdateDataFailedException

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
