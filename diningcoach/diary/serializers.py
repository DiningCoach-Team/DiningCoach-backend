from django.db import transaction, IntegrityError

from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from diary.exceptions import InvalidNumArgsException, UserInfoNotProvidedException, CreateDataFailedException

from rest_framework import serializers


##### Write, Edit, Delete Serializer #####
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


class MealDiaryWriteSerializer(serializers.Serializer):
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

  def set_meal_image(self, meal_image_list, meal_diary_id):
    if len(meal_image_list) > 5:
      raise InvalidNumArgsException(detail=('ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 이미지의 개수는 최대 5개입니다.'))

    for meal_image_data in meal_image_list:
      # meal_image_serializer = self.fields['meal_image']
      meal_image_serializer = MealImageWriteEditSerializer(data=meal_image_data, context=self.context)
      meal_image_serializer.context['parent_id'] = meal_diary_id
      meal_image_serializer.is_valid(raise_exception=True)
      meal_image_serializer.save()

  def set_meal_food(self, meal_food_list, meal_diary_id):
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

  @transaction.atomic
  def create(self, validated_data):
    request = self.context['request']

    if request and hasattr(request, 'user'):
      user_id = request.user.id
    else:
      raise UserInfoNotProvidedException(detail=('USER_NOT_PROVIDED', '유저 정보를 불러올 수 없습니다.'))

    try:
      with transaction.atomic():
        meal_diary = MealDiary.objects.create(
          date=validated_data['date'],
          meal_type=validated_data['meal_type'],
          content=validated_data['content'],
          is_favourite=validated_data['is_favourite'],
          is_public=validated_data['is_public'],
          is_deleted=self.IS_DELETED_DEFAULT,
          user_id=user_id,
        )
        # meal_diary.save()

        # max number of images : 5
        if ('meal_image' in validated_data) and (validated_data['meal_image'] is not None):
          self.set_meal_image(validated_data['meal_image'], meal_diary.id)
        # max number of food : 10
        if ('meal_food' in validated_data) and (validated_data['meal_food'] is not None):
          self.set_meal_food(validated_data['meal_food'], meal_diary.id)
    except IntegrityError:
      raise CreateDataFailedException(detail=('CREATE_DATA_FAILED', '식단일기 등록에 실패하였습니다. 다시 시도해주세요.'))

    return meal_diary
