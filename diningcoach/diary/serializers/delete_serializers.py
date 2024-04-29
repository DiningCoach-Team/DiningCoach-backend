from diary.models import MealDiary
from rest_framework import serializers


##### Delete Serializer #####
class MealDiaryDeleteSerializer(serializers.ModelSerializer):
  class Meta:
    model = MealDiary
    fields = '__all__'
