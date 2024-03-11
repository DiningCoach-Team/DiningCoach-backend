from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
  detail = None
  status_code = None

  def __init__(self, detail=None, code=None):
    super().__init__(detail, code)
    self.detail = detail
    self.status_code = code


class InvalidInputFormatException(BaseCustomException):
  def __init__(self, detail='데이터 입력 형식이 올바르지 않습니다.', code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class NoResultFoundException(BaseCustomException):
  def __init__(self, detail='찾으시는 내용이 없습니다.', code=status.HTTP_204_NO_CONTENT):
    super().__init__(detail, code)
