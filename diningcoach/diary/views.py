from django.shortcuts import render
from django.db.models import Prefetch

from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from diary.serializers import (
  MealDiaryDefaultSerializer,
  MealDiaryReadSerializer, MealDiaryWriteSerializer, MealDiaryEditSerializer, MealDiaryDeleteSerializer,
)
from diary.exceptions import NoMealDiaryFoundException, MultipleMealDiaryFoundException

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

  def get_queryset(self):
    self.kwargs[self.lookup_field] = self.request.user.id

    meal_diary = MealDiary.objects.filter(
      date__exact=self.kwargs['date'],
      meal_type__exact=self.kwargs['meal_type'],
      is_deleted__exact=False,
    ).prefetch_related(
      Prefetch('meal_image', queryset=MealImage.objects.filter(is_deleted__exact=False), to_attr='meal_image_data'),
      Prefetch('meal_food', queryset=MealFood.objects.all(), to_attr='meal_food_data'),
      Prefetch('meal_nutrition', queryset=MealNutrition.objects.all(), to_attr='meal_nutrition_data'),
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
    return super().delete(request, *args, **kwargs)


# 'api/diary/meal/<str:date>/<str:meal_type>/share?flag=?' -> GET
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
