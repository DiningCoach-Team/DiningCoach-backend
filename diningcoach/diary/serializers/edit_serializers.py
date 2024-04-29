import os
from datetime import datetime

from django.db import transaction, IntegrityError
from django.db.models import Prefetch

from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from diary.exceptions import (
  InvalidNumArgsException, UpdateDataFailedException,
)
from diary.serializers.base_serializers import (
  MealDiaryWriteEditSerializer, MealImageWriteEditSerializer, MealFoodWriteEditSerializer,
)
from diary.tasks import edit_meal_nutrition


##### Edit Serializer #####
class MealDiaryEditSerializer(MealDiaryWriteEditSerializer):
  date = None
  meal_type = None

  def edit_meal_image(self, old_list, new_list, meal_diary_id):
    if len(new_list) > 5:
      raise InvalidNumArgsException(detail=('D2', 'ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 이미지의 개수는 최대 5개입니다.'))

    # Convert data to list
    old_list = list(old_list)
    new_list = list(new_list)

    # Keep remaining images
    for old_data in old_list:
      old_filename = os.path.basename(str(old_data.image_url))

      for new_data in new_list:
        new_filename = str(new_data['image_url']).replace(' ', '_')

        if old_filename == new_filename:
          new_data['updated_at'] = datetime.now()

          meal_image_serializer = MealImageWriteEditSerializer(instance=old_data, data=new_data)
          meal_image_serializer.is_valid(raise_exception=True)
          meal_image_serializer.save()

          old_list.remove(old_data)
          new_list.remove(new_data)
          break

    # Delete old images
    for old_data in old_list:
      if not old_data.is_deleted:
        old_data.is_deleted = True
        old_data.save()

    # Save new images
    for new_data in new_list:
      # meal_image_serializer = self.fields['meal_image']
      meal_image_serializer = MealImageWriteEditSerializer(data=new_data, context=self.context)
      meal_image_serializer.context['parent_id'] = meal_diary_id
      meal_image_serializer.is_valid(raise_exception=True)
      meal_image_serializer.save()

  def edit_meal_food(self, old_list, new_list, meal_diary_id):
    if len(new_list) > 10:
      raise InvalidNumArgsException(detail=('D2', 'ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 음식의 개수는 최대 10개입니다.'))
    elif len(new_list) < 1:
      raise InvalidNumArgsException(detail=('D2', 'BELOW_MIN_NUM', '한 식단일기에 음식은 최소 1개 이상 등록해야 합니다.'))

    # Convert data to list
    old_list = list(old_list)
    new_list = list(new_list)

    # Keep remaining food
    for old_data in old_list:
      old_food_code = str(old_data.food_code)

      for new_data in new_list:
        new_food_code = str(new_data['food_code'])

        if old_food_code == new_food_code:
          old_list.remove(old_data)
          new_list.remove(new_data)
          break

    # Delete old food
    for old_data in old_list:
      old_data.delete()

    # Save new food
    for new_data in new_list:
      # meal_food_serializer = self.fields['meal_food']
      meal_food_serializer = MealFoodWriteEditSerializer(data=new_data, context=self.context)
      meal_food_serializer.context['parent_id'] = meal_diary_id
      meal_food_serializer.is_valid(raise_exception=True)
      meal_food_serializer.save()

  def update(self, instance, validated_data):
    # date = self.context['view'].kwargs['date']
    # meal_type = self.context['view'].kwargs['meal_type']
    # user_id = self.context['request'].user.id

    try:
      with transaction.atomic():
        meal_diary = MealDiary.objects.select_for_update().filter(
          id__exact=instance.id,
          is_deleted__exact=False,
        ).prefetch_related(
          Prefetch('meal_image', queryset=MealImage.objects.filter(is_deleted__exact=False)),
          Prefetch('meal_food', queryset=MealFood.objects.all()),
          Prefetch('meal_nutrition', queryset=MealNutrition.objects.all()),
        ).get()

        meal_diary.content = validated_data['content']
        meal_diary.is_favourite = validated_data['is_favourite']
        meal_diary.is_public = validated_data['is_public']
        meal_diary.is_deleted = self.IS_DELETED_DEFAULT

        meal_diary.save()

        # max number of images : 5
        if ('meal_image' in validated_data) and (validated_data['meal_image'] is not None):
          self.edit_meal_image(meal_diary.meal_image.all(), validated_data['meal_image'], meal_diary.id)
        # max number of food : 10
        if ('meal_food' in validated_data) and (validated_data['meal_food'] is not None):
          self.edit_meal_food(meal_diary.meal_food.all(), validated_data['meal_food'], meal_diary.id)
    except IntegrityError:
      raise UpdateDataFailedException(detail=('D5', 'UPDATE_DATA_FAILED', '식단일기 수정에 실패하였습니다. 다시 시도해주세요.'))

    # Celery asynchronous task
    edit_meal_nutrition.apply_async(kwargs={
      'meal_diary_id': meal_diary.id,
    })

    return meal_diary
