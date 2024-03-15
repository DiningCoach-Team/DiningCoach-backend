from food.models import CookedFood, CookedNutrition

from rest_framework import serializers


class CookedFoodSimpleSerializer(serializers.ModelSerializer):
  class Meta:
    model = CookedFood
    fields = ['id', 'food_name', 'category_main', 'category_sub', 'food_image', 'product_type']


class CookedFoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = CookedFood
    fields = '__all__'


class CookedNutritionSerializer(serializers.ModelSerializer):
  class Meta:
    model = CookedNutrition
    exclude = ['cooked_food']
