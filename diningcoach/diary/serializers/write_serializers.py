from django.db import transaction, IntegrityError

from diary.models import MealDiary
from diary.exceptions import (
  InvalidNumArgsException, UserInfoNotProvidedException, CreateDataFailedException, DuplicateMealDiaryException,
)
from diary.serializers.base_serializers import (
  MealDiaryWriteEditSerializer, MealImageWriteEditSerializer, MealFoodWriteEditSerializer,
)
from diary.tasks import write_meal_nutrition


##### Write Serializer #####
class MealDiaryWriteSerializer(MealDiaryWriteEditSerializer):
  def validate(self, attrs):
    request = self.context['request']

    if request and hasattr(request, 'user'):
      user_id = request.user.id
    else:
      raise UserInfoNotProvidedException(detail=('D3', 'USER_NOT_PROVIDED', '유저 정보를 불러올 수 없습니다.'))

    meal_diary = MealDiary.objects.filter(
      date__exact=attrs['date'],
      meal_type__exact=attrs['meal_type'],
      is_deleted__exact=False,
      user_id__exact=user_id,
    )
    if meal_diary.exists():
      raise DuplicateMealDiaryException(detail=('D7', 'DUPLICATE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 이미 존재합니다.'))
    return super().validate(attrs)

  def write_meal_image(self, meal_image_list, meal_diary_id):
    if len(meal_image_list) > 5:
      raise InvalidNumArgsException(detail=('D2', 'ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 이미지의 개수는 최대 5개입니다.'))

    for meal_image_data in meal_image_list:
      # meal_image_serializer = self.fields['meal_image']
      meal_image_serializer = MealImageWriteEditSerializer(data=meal_image_data, context=self.context)
      meal_image_serializer.context['parent_id'] = meal_diary_id
      meal_image_serializer.is_valid(raise_exception=True)
      meal_image_serializer.save()

  def write_meal_food(self, meal_food_list, meal_diary_id):
    if len(meal_food_list) > 10:
      raise InvalidNumArgsException(detail=('D2', 'ABOVE_MAX_NUM', '한 식단일기에 등록 가능한 음식의 개수는 최대 10개입니다.'))
    elif len(meal_food_list) < 1:
      raise InvalidNumArgsException(detail=('D2', 'BELOW_MIN_NUM', '한 식단일기에 음식은 최소 1개 이상 등록해야 합니다.'))

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
      raise CreateDataFailedException(detail=('D4', 'CREATE_DATA_FAILED', '식단일기 등록에 실패하였습니다. 다시 시도해주세요.'))

    # Celery asynchronous task
    write_meal_nutrition.apply_async(kwargs={
      'meal_diary_id': meal_diary.id,
    })

    return meal_diary
