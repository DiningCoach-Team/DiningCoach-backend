from rest_framework import status
from rest_framework.exceptions import APIException


class UserCustomException(APIException):
  detail = None
  status_code = None

  def __init__(self, detail=None, code=None):
    super().__init__(detail, code)
    self.detail = detail
    self.status_code = code


class InvalidNumArgsException(UserCustomException):
  def __init__(self, detail=('INVALID_NUM_ARGUMENTS', '올바른 인자의 개수가 아닙니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class UserInfoNotProvidedException(UserCustomException):
  def __init__(self, detail=('USER_NOT_PROVIDED', '유저 정보를 불러올 수 없습니다.'), code=status.HTTP_401_UNAUTHORIZED):
    super().__init__(detail, code)


class CreateDataFailedException(UserCustomException):
  def __init__(self, detail=('CREATE_DATA_FAILED', '데이터 생성에 실패하였습니다.'), code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    super().__init__(detail, code)


class DuplicateMealDiaryException(UserCustomException):
  def __init__(self, detail=('DUPLICATE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 이미 존재합니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)
