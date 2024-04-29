from food.exceptions import InvalidInputFormatException

from rest_framework import serializers


class FoodScanSerializer(serializers.Serializer):
  barcode_no = serializers.CharField(required=True)

  def validate_barcode_no(self, value):
    if not value.isnumeric():
      raise InvalidInputFormatException(detail=('F1', 'INVALID_FORMAT', '스캔하신 바코드의 입력 형식이 올바르지 않습니다.'))
    return value


class FoodSearchSerializer(serializers.Serializer):
  id = serializers.IntegerField(required=False)
  code = serializers.CharField(required=False)
  name = serializers.CharField(required=False)
  cate_main = serializers.CharField(required=False)
  cate_sub = serializers.CharField(required=False)
  # processed_food = ProcessedFoodSimpleSerializer(many=True, read_only=True)
  # fresh_food = FreshFoodSimpleSerializer(many=True, read_only=True)
  # cooked_food = CookedFoodSimpleSerializer(many=True, read_only=True)

  def validate(self, data):
    correct_query_params = ['id', 'code', 'name', 'cate_main', 'cate_sub']
    input_query_params = list(self.initial_data.keys())
    if not all(key in correct_query_params for key in input_query_params):
      raise InvalidInputFormatException(detail=('F1', 'INVALID_FORMAT', '입력하신 검색 조건 인자가 올바르지 않습니다.'))
    return data


class FoodDetailSerializer(serializers.Serializer):
  food_id = serializers.CharField(required=True)

  def validate_food_id(self, value):
    if not value.isnumeric():
      raise InvalidInputFormatException(detail=('F1', 'INVALID_FORMAT', '입력하신 식품 ID 형식이 올바르지 않습니다.'))
    return value
