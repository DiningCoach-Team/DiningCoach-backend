import re

from django.shortcuts import render
from django.db.models import Prefetch, F

from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from diary.serializers import (
  MealDiaryDefaultSerializer,
  MealDiaryReadSerializer, MealDiaryWriteSerializer, MealDiaryEditSerializer, MealDiaryDeleteSerializer,
)
from diary.exceptions import InvalidInputFormatException, NoMealDiaryFoundException, MultipleMealDiaryFoundException

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# 'api/diary/meal/' -> POST
class MealDiaryWriteView(CreateAPIView):
  queryset = MealDiary.objects.all()
  serializer_class = MealDiaryWriteSerializer
  permission_classes = [IsAuthenticated]


# 'api/diary/meal/<str:date>/<str:meal_type>/' -> GET, PUT, DELETE
class MealDiaryReadEditDeleteView(RetrieveUpdateDestroyAPIView):
  serializer_classes = {
    'GET': MealDiaryReadSerializer,
    'PUT': MealDiaryEditSerializer,
    'DELETE': MealDiaryDeleteSerializer,
  }

  serializer_class = MealDiaryDefaultSerializer
  permission_classes = [IsAuthenticated]
  lookup_field = 'user_id'

  def validate_input(self):
    date_input = self.kwargs['date']
    date_format = r'\b(19\d\d|20\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b'
    if not re.match(date_format, date_input):
      raise InvalidInputFormatException(detail=('INVALID_INPUT_FORMAT', '날짜 형식은 YYYY-MM-DD이 되어야 합니다.'))

    meal_type_input = self.kwargs['meal_type']
    if meal_type_input not in ['B', 'L', 'D', 'S']:
      raise InvalidInputFormatException(detail=('INVALID_INPUT_FORMAT', '식사 종류는 B,L,D,S 중에 하나가 되어야 합니다.'))

  def get_queryset(self):
    self.validate_input()
    self.kwargs[self.lookup_field] = self.request.user.id

    meal_diary = MealDiary.objects.filter(
      date__exact=self.kwargs['date'],
      meal_type__exact=self.kwargs['meal_type'],
      is_deleted__exact=False,
    ).prefetch_related(
      Prefetch('meal_image', queryset=MealImage.objects.filter(is_deleted__exact=False)),
      Prefetch('meal_food', queryset=MealFood.objects.all()),
      Prefetch('meal_nutrition', queryset=MealNutrition.objects.all()),
    )

    if not meal_diary.exists():
      raise NoMealDiaryFoundException(detail=('NO_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 존재하지 않습니다.'))
    elif meal_diary.count() > 1:
      raise MultipleMealDiaryFoundException(detail=('MULTIPLE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 2개 이상 존재합니다.'))

    return meal_diary

  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def get(self, request, *args, **kwargs):
    self.serializer_class = self.serializer_classes['GET']
    return super().get(request, *args, **kwargs)

  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def put(self, request, *args, **kwargs):
    self.serializer_class = self.serializer_classes['PUT']
    return super().put(request, *args, **kwargs)

  @swagger_auto_schema(auto_schema=None)
  def patch(self, request, *args, **kwargs):
    raise MethodNotAllowed(method='PATCH', detail='GET, PUT, 또는 DELETE 메서드 요청만 처리할 수 있습니다. (PATCH 요청 처리 불가)')

  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def delete(self, request, *args, **kwargs):
    self.serializer_class = self.serializer_classes['DELETE']

    instance = self.get_object()
    serializer = self.get_serializer(instance)

    if instance is not None:
      instance.is_deleted = ~F('is_deleted')
      instance.save()
      instance.refresh_from_db()

      if instance.is_deleted:
        return Response(data={'message': '식단일기가 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
      else:
        return Response(serializer.data)
    else:
      raise NoMealDiaryFoundException(detail=('NO_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 존재하지 않습니다.'))


# 'api/diary/meal/<str:date>/<str:meal_type>/share/' -> GET
class MealDiaryShareView(RetrieveAPIView):
  pass


'''
# 'api/diary/overview/summary/<str:date>/' -> GET
class DailySummaryView(RetrieveAPIView):
  pass


# 'api/diary/overview/nutrition/<str:date>/' -> GET
class DailyNutritionView(RetrieveAPIView):
  pass


# 'api/diary/overview/count/<int:year>/<int:month>/' -> GET
class MonthlyCountView(RetrieveAPIView):
  pass
'''
