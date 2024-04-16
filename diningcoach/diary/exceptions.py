from rest_framework import status
from rest_framework.exceptions import APIException


class UserCustomException(APIException):
  detail = None
  status_code = None

  def __init__(self, detail=None, code=None):
    super().__init__(detail, code)
    self.detail = detail
    self.status_code = code


class InvalidInputFormatException(UserCustomException):
  def __init__(self, detail=('INVALID_INPUT_FORMAT', '입력값의 형식이 올바르지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class InvalidNumArgsException(UserCustomException):
  def __init__(self, detail=('INVALID_NUM_ARGUMENTS', '올바른 인자의 개수가 아닙니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class UserInfoNotProvidedException(UserCustomException):
  def __init__(self, detail=('USER_NOT_PROVIDED', '유저 정보를 불러올 수 없습니다.'), code=status.HTTP_401_UNAUTHORIZED):
    super().__init__(detail, code)


class CreateDataFailedException(UserCustomException):
  def __init__(self, detail=('CREATE_DATA_FAILED', '데이터 생성에 실패하였습니다.'), code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    super().__init__(detail, code)


class UpdateDataFailedException(UserCustomException):
  def __init__(self, detail=('UPDATE_DATA_FAILED', '데이터 수정에 실패하였습니다.'), code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    super().__init__(detail, code)


class DeleteDataFailedException(UserCustomException):
  def __init__(self, detail=('DELETE_DATA_FAILED', '데이터 삭제에 실패하였습니다.'), code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    super().__init__(detail, code)


class DuplicateMealDiaryException(UserCustomException):
  def __init__(self, detail=('DUPLICATE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 이미 존재합니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class NoMealDiaryFoundException(UserCustomException):
  def __init__(self, detail=('NO_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 존재하지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class MultipleMealDiaryFoundException(UserCustomException):
  def __init__(self, detail=('MULTIPLE_MEAL_DIARY', '요청하신 날짜의 해당 식사에 대한 식단일기가 2개 이상 존재합니다.'), code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    super().__init__(detail, code)