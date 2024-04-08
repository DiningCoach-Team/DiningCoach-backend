from django.shortcuts import render

from diary.models import MealDiary
from diary.serializers import MealDiaryWriteSerializer

from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


# 'api/diary/meal/' -> POST
class MealDiaryWriteView(CreateAPIView):
  queryset = MealDiary.objects.all()
  serializer_class = MealDiaryWriteSerializer
  permission_classes = [IsAuthenticated]


# 'api/diary/meal/<str:date>/<str:meal_type>/' -> GET, PUT, DELETE
class MealDiaryReadEditDeleteView(RetrieveUpdateDestroyAPIView):
  pass


# 'api/diary/meal/<str:date>/<str:meal_type>/share?flag=?' -> GET
class MealDiaryShareView(RetrieveAPIView):
  pass


# 'api/diary/overview/summary/<str:date>/' -> GET
class DailySummaryView(RetrieveAPIView):
  pass


# 'api/diary/overview/nutrition/<str:date>/' -> GET
class DailyNutritionView(RetrieveAPIView):
  pass


# 'api/diary/overview/count/<int:year>/<int:month>/' -> GET
class MonthlyCountView(RetrieveAPIView):
  pass
