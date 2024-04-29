from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch, F

from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from diary.serializers.params_serializers import MealDiaryReadEditDeleteSerializer
from diary.serializers.base_serializers import MealDiaryDefaultSerializer
from diary.serializers.read_serializers import MealDiaryReadSerializer
from diary.serializers.write_serializers import MealDiaryWriteSerializer
from diary.serializers.edit_serializers import MealDiaryEditSerializer
from diary.serializers.delete_serializers import MealDiaryDeleteSerializer
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
  }

  serializer_class = MealDiaryDefaultSerializer
  permission_classes = [IsAuthenticated]
  lookup_field = 'user_id'

  def get_queryset(self):
    meal_diary = MealDiary.objects.filter(
      date__exact=self.kwargs['date'],
      meal_type__exact=self.kwargs['meal_type'],
      is_deleted__exact=False,
    ).prefetch_related(
      Prefetch('meal_image', queryset=MealImage.objects.filter(is_deleted__exact=False)),
      Prefetch('meal_food', queryset=MealFood.objects.all()),
      Prefetch('meal_nutrition', queryset=MealNutrition.objects.all()),
    )
    return meal_diary

  def get_object(self):
    self.kwargs[self.lookup_field] = self.request.user.id
    date_input = self.kwargs['date']
    meal_type_input = self.kwargs['meal_type']

    params_serializer = MealDiaryReadEditDeleteSerializer(data={'date': date_input, 'meal_type': meal_type_input})
    params_serializer.is_valid(raise_exception=True)

    queryset = self.filter_queryset(self.get_queryset())
    if not queryset.exists():
      raise NoMealDiaryFoundException(detail=('D8', 'NO_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 존재하지 않습니다.'))
    elif queryset.count() > 1:
      raise MultipleMealDiaryFoundException(detail=('D9', 'MULTIPLE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 2개 이상 존재합니다.'))

    filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
    obj = get_object_or_404(queryset, **filter_kwargs)

    self.check_object_permissions(self.request, obj)

    return obj

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
    instance = self.get_object()

    if instance is not None:
      instance.is_deleted = True
      instance.save()

      return Response(data={'message': '식단일기가 성공적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
    else:
      raise NoMealDiaryFoundException(detail=('D8', 'NO_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 존재하지 않습니다.'))


# 'api/diary/meal/<str:date>/<str:meal_type>/share/' -> GET
class MealDiaryShareView(MealDiaryReadEditDeleteView):
  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def get(self, request, *args, **kwargs):
    instance = self.get_object()

    if instance is not None:
      instance.is_public = ~F('is_public')
      instance.save()
      instance.refresh_from_db()

      if instance.is_public:
        return Response(data={'message': '식단일기가 공개로 전환되었습니다.'}, status=status.HTTP_200_OK)
      else:
        return Response(data={'message': '식단일기가 비공개로 전환되었습니다.'}, status=status.HTTP_200_OK)
    else:
      raise NoMealDiaryFoundException(detail=('D8', 'NO_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 존재하지 않습니다.'))

  @swagger_auto_schema(auto_schema=None)
  def put(self, request, *args, **kwargs):
    raise MethodNotAllowed(method='PUT', detail='GET 메서드 요청만 처리할 수 있습니다. (POST, PUT, PATCH, DELETE 요청 처리 불가)')

  @swagger_auto_schema(auto_schema=None)
  def patch(self, request, *args, **kwargs):
    raise MethodNotAllowed(method='PATCH', detail='GET 메서드 요청만 처리할 수 있습니다. (POST, PUT, PATCH, DELETE 요청 처리 불가)')

  @swagger_auto_schema(auto_schema=None)
  def delete(self, request, *args, **kwargs):
    raise MethodNotAllowed(method='DELETE', detail='GET 메서드 요청만 처리할 수 있습니다. (POST, PUT, PATCH, DELETE 요청 처리 불가)')


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
