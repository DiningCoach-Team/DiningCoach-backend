from rest_framework import status
from rest_framework.exceptions import APIException


class UserCustomException(APIException):
  detail = None
  status_code = None

  def __init__(self, detail=None, code=None):
    super().__init__(detail, code)
    self.detail = detail
    self.status_code = code


class InvalidUsernameFormatException(UserCustomException):
  def __init__(self, detail=('INVALID_USERNAME', '이름(사용자명) 입력 형식이 올바르지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class InvalidEmailFormatException(UserCustomException):
  def __init__(self, detail=('INVALID_EMAIL', '이메일 입력 형식이 올바르지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class InvalidPasswordFormatException(UserCustomException):
  def __init__(self, detail=('INVALID_PASSWORD', '비밀번호 입력 형식이 올바르지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class AccountAlreadyExistsException(UserCustomException):
  def __init__(self, detail=('ACCOUNT_ALREADY_EXISTS', '해당 이메일로 등록된 계정이 이미 존재합니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class AccountNotExistsException(UserCustomException):
  def __init__(self, detail=('ACCOUNT_NOT_EXISTS', '해당 이메일로 등록된 계정이 존재하지 않습니다.'), code=status.HTTP_400_BAD_REQUEST):
    super().__init__(detail, code)


class AuthenticationFailedException(UserCustomException):
  def __init__(self, detail=('AUTHENTICATION_FAILED', '인증에 실패하였습니다.'), code=status.HTTP_401_UNAUTHORIZED):
    super().__init__(detail, code)


class CreateDataFailedException(UserCustomException):
  def __init__(self, detail=('CREATE_DATA_FAILED', '데이터 생성에 실패하였습니다.'), code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    super().__init__(detail, code)


class UpdateNotAllowedException(UserCustomException):
  def __init__(self, detail=('UPDATE_NOT_ALLOWED', '데이터를 변경할 권한이 없습니다.'), code=status.HTTP_401_UNAUTHORIZED):
    super().__init__(detail, code)
