from food.models import ProcessedFood, ProcessedNutrition

from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework import status


class ProcessedFoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProcessedFood
    fields = '__all__'

  # def validate(self, attrs):
  #   barcode_no = self.get_extra_kwargs('barcode_no')

  #   if not barcode_no.isnumeric():
  #     raise ValidationError(message='바코드 형식이 올바르지 않습니다.', code=status.HTTP_400_BAD_REQUEST)

  #   return super().validate(attrs)


class ProcessedNutritionSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProcessedNutrition
    exclude = ['processed_food']


class FoodScanSerializer(serializers.ModelSerializer):
  nutrition_info = ProcessedNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = ProcessedFood
    fields = '__all__'
