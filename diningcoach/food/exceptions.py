from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
  detail = None
  code = None

  def __init__(self, detail=None, code=None):
    super().__init__(detail, code)
    self.detail = detail
    self.code = code
