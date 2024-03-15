from food.models import ProcessedFood, FreshFood, CookedFood
from food.serializers.processed_serializers import ProcessedNutritionSerializer
from food.serializers.fresh_serializers import FreshNutritionSerializer
from food.serializers.cooked_serializers import CookedNutritionSerializer

from rest_framework import serializers


class ProcessedFoodDetailSerializer(serializers.ModelSerializer):
  nutrition_info = ProcessedNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = ProcessedFood
    fields = '__all__'


class FreshFoodDetailSerializer(serializers.ModelSerializer):
  nutrition_info = FreshNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = FreshFood
    fields = '__all__'


class CookedFoodDetailSerializer(serializers.ModelSerializer):
  nutrition_info = CookedNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = CookedFood
    fields = '__all__'
