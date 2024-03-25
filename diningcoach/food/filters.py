from food.models import ProcessedFood, FreshFood, CookedFood
from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter


class FoodFilter(FilterSet):
  no = NumberFilter(field_name='id', lookup_expr='exact')
  code = CharFilter(field_name='food_code', lookup_expr='contains')
  name = CharFilter(field_name='food_name', lookup_expr='contains')
  cate_main = CharFilter(field_name='category_main', lookup_expr='iexact')
  cate_sub = CharFilter(field_name='category_sub', lookup_expr='iexact')


class ProcessedFoodFilter(FoodFilter):
  class Meta:
    model = ProcessedFood
    fields = ['no', 'code', 'name', 'cate_main', 'cate_sub']


class FreshFoodFilter(FoodFilter):
  class Meta:
    model = FreshFood
    fields = ['no', 'code', 'name', 'cate_main', 'cate_sub']


class CookedFoodFilter(FoodFilter):
  class Meta:
    model = CookedFood
    fields = ['no', 'code', 'name', 'cate_main', 'cate_sub']
