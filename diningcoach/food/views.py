from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ValidationError

from food.models import ProcessedFood, FreshFood, CookedFood
from food.serializers.params_serializers import FoodScanSerializer, FoodSearchSerializer, FoodDetailSerializer
from food.serializers.processed_serializers import ProcessedFoodSimpleSerializer, ProcessedFoodDetailSerializer
from food.serializers.fresh_serializers import FreshFoodSimpleSerializer, FreshFoodDetailSerializer
from food.serializers.cooked_serializers import CookedFoodSimpleSerializer, CookedFoodDetailSerializer
from food.exceptions import InvalidInputFormatException, NoResultFoundException
from food.filters import ProcessedFoodFilter, FreshFoodFilter, CookedFoodFilter

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


# api/food/scan/<str:barcode_no>/
class FoodScanView(ListAPIView):
  serializer_class = ProcessedFoodDetailSerializer

  def get_queryset(self, barcode_no):
    food_list = ProcessedFood.objects.filter(barcode_no=barcode_no)
    return food_list

  def list(self, request, *args, **kwargs):
    barcode_no = self.kwargs['barcode_no']

    params_serializer = FoodScanSerializer(data={'barcode_no': barcode_no})
    params_serializer.is_valid(raise_exception=True)

    queryset = self.filter_queryset(self.get_queryset(barcode_no))
    if not queryset.exists():
      raise NoResultFoundException(detail=('F2', 'NO_RESULT', '스캔하신 바코드에 해당하는 식품이 존재하지 않습니다.'))

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  # def get_object(self, barcode_no):
  #   try:
  #     return ProcessedFood.objects.get(barcode_no=barcode_no)
  #   except ProcessedFood.DoesNotExist:
  #     raise Http404
  #
  # def get(self, request, barcode_no, format=None):
  #   scan_result = self.get_object(barcode_no)
  #   serializer = ProcessedFoodSerializer(scan_result, many=True)
  #   return Response(serializer.data)


# 'Food Search' base class
class FoodSearchView(ListAPIView):
  filter_backends = [DjangoFilterBackend]

  def list(self, request, *args, **kwargs):
    params_serializer = FoodSearchSerializer(data=request.query_params)
    params_serializer.is_valid(raise_exception=True)

    queryset = self.filter_queryset(self.get_queryset())
    if not queryset.exists():
      raise NoResultFoundException(detail=('F2', 'NO_RESULT', '검색하신 조건에 해당하는 식품이 존재하지 않습니다.'))

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)


# api/food/search/processed?id=?&code=?&name=?&cate_main=?&cate_sub=?
class ProcessedFoodSearchView(FoodSearchView):
  queryset = ProcessedFood.objects.all()
  serializer_class = ProcessedFoodSimpleSerializer
  filterset_class = ProcessedFoodFilter


# api/food/search/fresh?id=?&code=?&name=?&cate_main=?&cate_sub=?
class FreshFoodSearchView(FoodSearchView):
  queryset = FreshFood.objects.all()
  serializer_class = FreshFoodSimpleSerializer
  filterset_class = FreshFoodFilter


# api/food/search/cooked?id=?&code=?&name=?&cate_main=?&cate_sub=?
class CookedFoodSearchView(FoodSearchView):
  queryset = CookedFood.objects.all()
  serializer_class = CookedFoodSimpleSerializer
  filterset_class = CookedFoodFilter


# 'Food Detail' base class
class FoodDetailView(RetrieveAPIView):
  lookup_field = 'id'

  def retrieve(self, request, *args, **kwargs):
    food_id = self.kwargs['id']

    params_serializer = FoodDetailSerializer(data={'food_id': food_id})
    params_serializer.is_valid(raise_exception=True)

    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response(serializer.data)


# api/food/detail/processed/<str:id>/
class ProcessedFoodDetailView(FoodDetailView):
  queryset = ProcessedFood.objects.all()
  serializer_class = ProcessedFoodDetailSerializer


# api/food/detail/fresh/<str:id>/
class FreshFoodDetailView(FoodDetailView):
  queryset = FreshFood.objects.all()
  serializer_class = FreshFoodDetailSerializer


# api/food/detail/cooked/<str:id>/
class CookedFoodDetailView(FoodDetailView):
  queryset = CookedFood.objects.all()
  serializer_class = CookedFoodDetailSerializer
