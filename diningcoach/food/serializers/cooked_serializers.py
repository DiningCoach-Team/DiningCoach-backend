from food.models import CookedFood, CookedNutrition

from rest_framework import serializers


class CookedNutritionSerializer(serializers.ModelSerializer):
  class Meta:
    model = CookedNutrition
    exclude = ['cooked_food']


class CookedFoodDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = CookedFood
    fields = '__all__'


class CookedFoodSimpleSerializer(serializers.ModelSerializer):
  class Meta:
    model = CookedFood
    fields = ['id', 'food_name', 'category_main', 'category_sub', 'food_image', 'product_type']


class CookedFoodDetailSerializer(serializers.ModelSerializer):
  nutrition_info = CookedNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = CookedFood
    fields = '__all__'
