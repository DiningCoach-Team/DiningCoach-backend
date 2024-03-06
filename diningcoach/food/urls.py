from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from food.views import (
  FoodScanView, FoodSearchView
)

urlpatterns = [
  path('scan/<str:barcode_no>', FoodScanView.as_view()),
  path('search', FoodSearchView.as_view()), # query parameter : type, code, name, main, sub
]

urlpatterns = format_suffix_patterns(urlpatterns)
