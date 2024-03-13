from food.models import ProcessedFood
from food.serializers.processed_serializers import ProcessedNutritionSerializer

from rest_framework import serializers


class ProcessedFoodDetailSerializer(serializers.Serializer):
  nutrition_info = ProcessedNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = ProcessedFood
    fields = '__all__'
