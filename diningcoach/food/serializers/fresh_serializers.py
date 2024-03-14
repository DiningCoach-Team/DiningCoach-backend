from food.models import FreshFood, FreshNutrition

from rest_framework import serializers


class FreshFoodSimpleSerializer(serializers.ModelSerializer):
  class Meta:
    model = FreshFood
    fields = ['id', 'food_name', 'category_main', 'category_sub', 'food_image', 'harvest_time']


class FreshFoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = FreshFood
    fields = '__all__'


class FreshNutritionSerializer(serializers.ModelSerializer):
  class Meta:
    model = FreshNutrition
    exclude = ['fresh_food']
