from diary.models import MealDiary, MealImage, MealFood, MealNutrition
from rest_framework import serializers


##### Read Serializer #####
class MealImageReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealImage
    exclude = ['device_info', 'is_deleted', 'meal']


class MealFoodReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealFood
    exclude = ['meal']


class MealNutritionReadSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealNutrition
    exclude = ['meal']


class MealDiaryReadSerializer(serializers.ModelSerializer):
  meal_image = MealImageReadSerializer(many=True, read_only=True)
  meal_food = MealFoodReadSerializer(many=True, read_only=True)
  meal_nutrition = MealNutritionReadSerializer(many=False, read_only=True)

  class Meta:
    model = MealDiary
    fields = '__all__'
