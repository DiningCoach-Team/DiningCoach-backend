from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from food.views import (
  FoodScanView, ProcessedFoodSearchView, FreshFoodSearchView, CookedFoodSearchView
)

urlpatterns = [
  path('scan/<str:barcode_no>/', FoodScanView.as_view()),

  # query parameter : no, code, name, cate_main, cate_sub
  path('search/processed', ProcessedFoodSearchView.as_view()),
  path('search/fresh', FreshFoodSearchView.as_view()),
  path('search/cooked', CookedFoodSearchView.as_view()),

  # path('detail/processed', ProcessedFoodDetailView.as_view()),
  # path('detail/fresh', FreshFoodDetailView.as_view()),
  # path('detail/cooked', CookedFoodDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
