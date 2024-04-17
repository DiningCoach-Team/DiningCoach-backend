import os
from datetime import datetime

from django.db import transaction, IntegrityError
from django.db.models import Prefetch

from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from diary.exceptions import (
  InvalidNumArgsException, UserInfoNotProvidedException,
  CreateDataFailedException, UpdateDataFailedException, DuplicateMealDiaryException,
)
from diary.tasks import write_meal_nutrition, edit_meal_nutrition

from rest_framework import serializers


##### Default Serializer #####
class MealImageDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealImage
    fields = '__all__'


class MealFoodDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealFood
    fields = '__all__'


class MealDiaryDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealDiary
    fields = '__all__'


##### Read Serializer #####
class MealImageReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealImage
    exclude = ['device_info', 'is_deleted', 'meal']


class MealFoodReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealFood
    exclude = ['meal']


class MealNutritionReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealNutrition
    exclude = ['meal']


class MealDiaryReadSerializer(serializers.ModelSerializer):
  meal_image = MealImageReadSerializer(many=True, read_only=True)
  meal_food = MealFoodReadSerializer(many=True, read_only=True)
  meal_nutrition = MealNutritionReadSerializer(many=False, read_only=True)

  class Meta:
    model = MealDiary
    fields = '__all__'


##### Write & Edit Serializer #####
class MealImageWriteEditSerializer(serializers.ModelSerializer):
  IS_DELETED_DEFAULT = False

  image_url = serializers.ImageField(required=True, label='이미지 주소', use_url=True)
  is_deleted = serializers.BooleanField(required=False, label='삭제 여부', default=IS_DELETED_DEFAULT)

  class Meta:
    model = MealImage
    fields = ['image_url', 'is_deleted']

  def create(self, validated_data):
    meal_image = MealImage.objects.create(
      image_url=validated_data['image_url'],
      device_info=self.context['request'].META['HTTP_USER_AGENT'],
      is_deleted=self.IS_DELETED_DEFAULT,
      meal_id=self.context['parent_id'],
    )
    return meal_image

  def update(self, instance, validated_data):
    return super().update(instance, validated_data)


class MealFoodWriteEditSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealFood
    exclude = ['meal']

  def create(self, validated_data):
    meal_food = MealFood.objects.create(
      meal_id=self.context['parent_id'],
      **validated_data,
    )
    return meal_food

  def update(self, instance, validated_data):
    return super().update(instance, validated_data)


class MealDiaryWriteEditSerializer(serializers.Serializer):
  MEAL_TYPES = [
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
    ('S', 'Snack'),
  ]
  IS_FAVOURITE_DEFAULT = False
  IS_PUBLIC_DEFAULT = False
  IS_DELETED_DEFAULT = False

  date         = serializers.DateField(required=True, label='식단일기 날짜')
  meal_type    = serializers.ChoiceField(required=True, label='식사 종류', choices=MEAL_TYPES)
  content      = serializers.CharField(required=False, label='내용', allow_blank=True, allow_null=True)
  is_favourite = serializers.BooleanField(required=False, label='즐겨찾기', default=IS_FAVOURITE_DEFAULT)
  is_public    = serializers.BooleanField(required=False, label='공개 여부', default=IS_PUBLIC_DEFAULT)
  is_deleted   = serializers.BooleanField(required=False, label='삭제 여부', default=IS_DELETED_DEFAULT)

  meal_image = MealImageWriteEditSerializer(required=False, many=True, read_only=False)
  meal_food  = MealFoodWriteEditSerializer(required=True, many=True, read_only=False)


##### Write Serializer #####
class MealDiaryWriteSerializer(MealDiaryWriteEditSerializer):
  def validate(self, attrs):
    request = self.context['request']

    if request and hasattr(request, 'user'):
      user_id = request.user.id
    else:
      raise UserInfoNotProvidedException(detail=('USER_NOT_PROVIDED', '유저 정보를 불러올 수 없습니다.'))

    meal_diary = MealDiary.objects.filter(
      date__exact=attrs['date'],
      meal_type__exact=attrs['meal_type'],
      is_deleted__exact=False,
      user_id__exact=user_id,
    )
    if meal_diary.exists():
      raise DuplicateMealDiaryException(detail=('DUPLICATE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 이미 존재합니다.'))
    return super().validate(attrs)

  def write_meal_image(self, meal_image_list, meal_diary_id):
    if len(meal_image_list) > 5:
      raise InvalidNumArgsException(detail=('ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 이미지의 개수는 최대 5개입니다.'))

    for meal_image_data in meal_image_list:
      # meal_image_serializer = self.fields['meal_image']
      meal_image_serializer = MealImageWriteEditSerializer(data=meal_image_data, context=self.context)
      meal_image_serializer.context['parent_id'] = meal_diary_id
      meal_image_serializer.is_valid(raise_exception=True)
      meal_image_serializer.save()

  def write_meal_food(self, meal_food_list, meal_diary_id):
    if len(meal_food_list) > 10:
      raise InvalidNumArgsException(detail=('ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 음식의 개수는 최대 10개입니다.'))
    elif len(meal_food_list) < 1:
      raise InvalidNumArgsException(detail=('BELOW_MIN_NUM', '한 식단일기에 음식은 최소 1개 이상 등록해야 합니다.'))

    for meal_food_data in meal_food_list:
      # meal_food_serializer = self.fields['meal_food']
      meal_food_serializer = MealFoodWriteEditSerializer(data=meal_food_data, context=self.context)
      meal_food_serializer.context['parent_id'] = meal_diary_id
      meal_food_serializer.is_valid(raise_exception=True)
      meal_food_serializer.save()

  def create(self, validated_data):
    user_id = self.context['request'].user.id

    try:
      with transaction.atomic():
        meal_diary = MealDiary.objects.select_for_update().get_or_create(
          date=validated_data['date'],
          meal_type=validated_data['meal_type'],
          content=validated_data['content'],
          is_favourite=validated_data['is_favourite'],
          is_public=validated_data['is_public'],
          is_deleted=self.IS_DELETED_DEFAULT,
          user_id=user_id,
        )
        meal_diary = meal_diary[0]
        # meal_diary.save()

        # max number of images : 5
        if ('meal_image' in validated_data) and (validated_data['meal_image'] is not None):
          self.write_meal_image(validated_data['meal_image'], meal_diary.id)
        # max number of food : 10
        if ('meal_food' in validated_data) and (validated_data['meal_food'] is not None):
          self.write_meal_food(validated_data['meal_food'], meal_diary.id)
    except IntegrityError:
      raise CreateDataFailedException(detail=('CREATE_DATA_FAILED', '식단일기 등록에 실패하였습니다. 다시 시도해주세요.'))

    # Celery asynchronous task
    write_meal_nutrition.apply_async(kwargs={
      'meal_diary_id': meal_diary.id,
    })

    return meal_diary


##### Edit Serializer #####
class MealDiaryEditSerializer(MealDiaryWriteEditSerializer):
  date = None
  meal_type = None

  def edit_meal_image(self, old_list, new_list, meal_diary_id):
    if len(new_list) > 5:
      raise InvalidNumArgsException(detail=('ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 이미지의 개수는 최대 5개입니다.'))

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
      raise InvalidNumArgsException(detail=('ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 음식의 개수는 최대 10개입니다.'))
    elif len(new_list) < 1:
      raise InvalidNumArgsException(detail=('BELOW_MIN_NUM', '한 식단일기에 음식은 최소 1개 이상 등록해야 합니다.'))

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
      raise UpdateDataFailedException(detail=('UPDATE_DATA_FAILED', '식단일기 수정에 실패하였습니다. 다시 시도해주세요.'))

    # Celery asynchronous task
    edit_meal_nutrition.apply_async(kwargs={
      'meal_diary_id': meal_diary.id,
    })

    return meal_diary


##### Delete Serializer #####
class MealDiaryDeleteSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealDiary
    fields = '__all__'
