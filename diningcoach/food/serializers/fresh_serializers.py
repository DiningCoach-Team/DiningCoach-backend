from food.models import FreshFood, FreshNutrition

from rest_framework import serializers


class FreshNutritionSerializer(serializers.ModelSerializer):
  class Meta:
    model = FreshNutrition
    exclude = ['fresh_food']


class FreshFoodDefaultSerializer(serializers.ModelSerializer):
  class Meta:
    model = FreshFood
    fields = '__all__'


class FreshFoodSimpleSerializer(serializers.ModelSerializer):
  class Meta:
    model = FreshFood
    fields = ['id', 'food_name', 'category_main', 'category_sub', 'food_image', 'harvest_time']


class FreshFoodDetailSerializer(serializers.ModelSerializer):
  nutrition_info = FreshNutritionSerializer(many=False, read_only=True)

  class Meta:
    model = FreshFood
    fields = '__all__'
