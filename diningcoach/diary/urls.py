from django.urls import path, include

from diary.views import (
  MealDiaryWriteView, MealDiaryReadEditDeleteView, MealDiaryShareView,
)

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
  path('meal/', MealDiaryWriteView.as_view(), name='diary_write'),
  path('meal/<str:date>/<str:meal_type>/', MealDiaryReadEditDeleteView.as_view(), name='diary_read_edit_delete'),
  path('meal/<str:date>/<str:meal_type>/share/', MealDiaryShareView.as_view(), name='diary_share'),

  # path('overview/summary/<str:date>/', DailySummaryView.as_view(), name='overview_summary'),
  # path('overview/nutrition/<str:date>/', DailyNutritionView.as_view(), name='overview_nutrition'),
  # path('overview/count/<int:year>/<int:month>/', MonthlyCountView.as_view(), name='overview_count'),
]
