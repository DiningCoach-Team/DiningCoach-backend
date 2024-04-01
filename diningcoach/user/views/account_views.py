from jwt import decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import update_last_login

from user.models import User, UserProfile, UserHealth
from user.serializers import UserSignUpSerializer, UserLoginSerializer
from user.exceptions import CreateDataFailedException

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


# POST 'api/user/account/signup/'
class UserSignUpView(GenericAPIView):
  serializer_class = UserSignUpSerializer

  def save_related(self, user):
    try:
      user_id = getattr(user, 'id')
    except AttributeError:
      raise CreateDataFailedException(detail=('CREATE_DATA_FAILED', '회원 데이터는 성공적으로 생성되었으나, 프로필 데이터와 건강 데이터 생성에는 실패하였습니다.'))

    user_profile = UserProfile.objects.create(
      user_id=user_id,
      consent_terms=False,
      receive_marketing=False,
    )
    user_profile.save()

    user_health = UserHealth.objects.create(
      user_id=user_id,
    )
    user_health.save()

    return user

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data, context=request)

    if serializer.is_valid(raise_exception=True):
      user = serializer.save()

      self.save_related(user)

      token = TokenObtainPairSerializer.get_token(user)
      refresh_token = str(token)
      access_token = str(token.access_token)

      res_data = {
        'user': serializer.data,
        'message': 'Sign Up Successful!',
        'access_token': access_token,
        'refresh_token': refresh_token,
      }

      response = Response(res_data, status=status.HTTP_201_CREATED)
      response.set_cookie('access_token', access_token, httponly=True)
      response.set_cookie('refresh_token', refresh_token, httponly=True)

      return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# POST 'api/user/account/login/'
class UserLoginView(GenericAPIView):
  serializer_class = UserLoginSerializer

  def post(self, request, *args, **kwargs):
    # user = authenticate(email=request.data['email'], password=request.data['password'])
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid(raise_exception=True):
      user = User.objects.get(email=request.data['email'])
      update_last_login(None, user)

      token = TokenObtainPairSerializer.get_token(user)
      refresh_token = str(token)
      access_token = str(token.access_token)

      res_data = {
        'user': serializer.data,
        'message': 'Login Successful!',
        'access_token': access_token,
        'refresh_token': refresh_token,
      }

      response = Response(res_data, status=status.HTTP_200_OK)
      response.set_cookie('access_token', access_token, httponly=True)
      response.set_cookie('refresh_token', refresh_token, httponly=True)

      return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE 'api/user/account/logout/'
class UserLogoutView(GenericAPIView):
  permission_classes = [IsAuthenticated]

  def delete(self, request, *args, **kwargs):
    res_data = {
      'message': 'Logout Successful!'
    }

    response = Response(res_data, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response


# GET 'api/user/account/token/refresh/' -> deprecated
class CustomizedTokenRefreshView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    # 토큰이 아직 유효한 경우
    try:
      access_token = request.COOKIES['access_token']
      decode(access_token, settings.SECRET_KEY, algorithms=['HS256']) # returns payload

      res_data = {
        'message': '토큰이 아직 만료되지 않았으므로 갱신할 필요가 없습니다.'
      }
      response = Response(res_data, status=status.HTTP_400_BAD_REQUEST)
    # 토큰이 만료된 경우
    except ExpiredSignatureError:
      refresh_token = request.COOKIES['refresh_token']
      serializer = TokenRefreshSerializer(data={'refresh': refresh_token})

      if serializer.is_valid(raise_exception=True):
        access_token = serializer.data['access']
        refresh_token = serializer.data['refresh']
        decode(access_token, settings.SECRET_KEY, algorithms=['HS256']) # returns payload

        res_data = {
          'message': '토큰이 정상적으로 갱신되었습니다.'
        }
        response = Response(res_data, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)
      else:
        raise InvalidTokenError
    # 토큰이 사용 불가한 경우
    except InvalidTokenError:
      res_data = {
        'message': '토큰이 사용 불가하므로 갱신할 수 없습니다.'
      }
      response = Response(res_data, status=status.HTTP_400_BAD_REQUEST)

    return response
