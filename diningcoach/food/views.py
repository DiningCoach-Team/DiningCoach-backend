from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ValidationError

from food.models import ProcessedFood
from food.serializers import FoodScanSerializer
from food.exceptions import InvalidInputFormatException, NoResultFoundException

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status


# api/food/scan/<str:barcode_no>
class FoodScanView(ListAPIView):
  serializer_class = FoodScanSerializer

  def validate(self, barcode_no):
    if not barcode_no.isnumeric():
      raise InvalidInputFormatException(detail='스캔하신 바코드의 입력 형식이 올바르지 않습니다.', code=status.HTTP_400_BAD_REQUEST)

  def get_queryset(self):
    barcode_no = self.kwargs['barcode_no']
    self.validate(barcode_no)

    return ProcessedFood.objects.filter(barcode_no=barcode_no)

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    if not queryset.exists():
      raise NoResultFoundException(detail='스캔하신 바코드에 해당하는 상품이 존재하지 않습니다.', code=status.HTTP_204_NO_CONTENT)

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


# api/food/search/?
class FoodSearchView(APIView):
  def get(self):
    pass
