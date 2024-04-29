import re
from diary.exceptions import InvalidInputFormatException
from rest_framework import serializers

##### Params Serializer #####
class MealDiaryReadEditDeleteSerializer(serializers.Serializer):
  date = serializers.CharField(required=True)
  meal_type = serializers.CharField(required=True)

  def validate_date(self, value):
    date_format = r'\b(19\d\d|20\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b'
    if not re.match(date_format, value):
      raise InvalidInputFormatException(detail=('D1', 'INVALID_INPUT_FORMAT', '날짜 형식은 YYYY-MM-DD이 되어야 합니다.'))

  def validate_meal_type(self, value):
    if value not in ['B', 'L', 'D', 'S']:
      raise InvalidInputFormatException(detail=('D1', 'INVALID_INPUT_FORMAT', '식사 종류는 B,L,D,S 중에 하나가 되어야 합니다.'))
