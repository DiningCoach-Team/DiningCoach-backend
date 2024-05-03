from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from food.views import (
  FoodScanView,
  ProcessedFoodSearchView, FreshFoodSearchView, CookedFoodSearchView,
  ProcessedFoodDetailView, FreshFoodDetailView, CookedFoodDetailView,
)

urlpatterns = [
  path('scan/<str:barcode_no>/', FoodScanView.as_view(), name='scan_barcode'),

  # query parameter : id, code, name, cate_main, cate_sub
  path('search/processed', ProcessedFoodSearchView.as_view(), name='search_processed'),
  path('search/fresh', FreshFoodSearchView.as_view(), name='search_fresh'),
  path('search/cooked', CookedFoodSearchView.as_view(), name='search_cooked'),

  path('detail/processed/<str:id>/', ProcessedFoodDetailView.as_view(), name='detail_processed'),
  path('detail/fresh/<str:id>/', FreshFoodDetailView.as_view(), name='detail_fresh'),
  path('detail/cooked/<str:id>/', CookedFoodDetailView.as_view(), name='detail_cooked'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
