from food.models import ProcessedFood, FreshFood, CookedFood
from food.serializers.processed_serializers import ProcessedFoodSimpleSerializer
from food.serializers.fresh_serializers import FreshFoodSimpleSerializer
from food.serializers.cooked_serializers import CookedFoodSimpleSerializer

from rest_framework import serializers


# Not used
class FoodSearchSerializer(serializers.Serializer):
  processed_food = ProcessedFoodSimpleSerializer(many=True, read_only=True)
  fresh_food = FreshFoodSimpleSerializer(many=True, read_only=True)
  cooked_food = CookedFoodSimpleSerializer(many=True, read_only=True)
