from diary.models import MealDiary, MealImage, MealFood, MealNutrition
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


class MealNutritionDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealNutrition
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
    try:
      device_info = self.context['request'].META['HTTP_USER_AGENT']
    except KeyError:
      device_info = 'Unknown Device'

    meal_image = MealImage.objects.create(
      image_url=validated_data['image_url'],
      device_info=device_info,
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
