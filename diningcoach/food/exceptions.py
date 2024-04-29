from rest_framework import status
from rest_framework.exceptions import APIException


class FoodCustomException(APIException):
  detail = None
  status_code = None

  def __init__(self, detail=None, code=None):
    super().__init__(detail, code)
    self.detail = detail
    self.status_code = code


class InvalidInputFormatException(FoodCustomException):
  def __init__(self, detail=('F1', 'INVALID_FORMAT', '데이터 입력 형식이 올바르지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class NoResultFoundException(FoodCustomException):
  def __init__(self, detail=('F2', 'NO_RESULT', '찾으시는 내용이 없습니다.'), code=status.HTTP_404_NOT_FOUND):
    super().__init__(detail, code)
