from django.urls import path, include

from diary.views import (
  MealDiaryWriteView, MealDiaryReadEditDeleteView, MealDiaryShareView,
  DailySummaryView, DailyNutritionView, MonthlyCountView,
)

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
  path('meal/', MealDiaryWriteView.as_view()),
  path('meal/<str:date>/<str:meal_type>/', MealDiaryReadEditDeleteView.as_view()),
  path('meal/<str:date>/<str:meal_type>/share', MealDiaryShareView.as_view()), # query parameter : flag

  path('overview/summary/<str:date>/', DailySummaryView.as_view()),
  path('overview/nutrition/<str:date>/', DailyNutritionView.as_view()),
  path('overview/count/<int:year>/<int:month>/', MonthlyCountView.as_view()),
]
