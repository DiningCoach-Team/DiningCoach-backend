from django.shortcuts import render
from django.contrib.auth.models import update_last_login

from user.models import User
from user.serializers import UserSignUpSerializer, UserLoginSerializer

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


# api/user/account/signup/
class UserSignUpView(GenericAPIView):
  serializer_class = UserSignUpSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data)

    if serializer.is_valid(raise_exception=True):
      user = serializer.save()

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


# api/user/account/login/
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


# api/user/account/logout/
class UserLogoutView(GenericAPIView):
  def delete(self, request, *args, **kwargs):
    res_data = {
      'message': 'Logout Successful!'
    }

    response = Response(res_data, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response


# api/user/account/token/refresh/
class CustomizedTokenRefreshView(GenericAPIView):
  pass


# api/user/auth/kakao/
class KakaoSignInView(APIView):
  pass


# api/user/auth/google/
class GoogleSignInView(APIView):
  pass


# api/user/auth/apple/
class AppleSignInView(APIView):
  pass


# api/user/auth/naver/
class NaverSignInView(APIView):
  pass


# api/user/info/profile/
class UserProfileView(APIView):
  pass


# api/user/info/health/
class UserHealthView(APIView):
  pass


# api/user/info/consent/
class ConsentTermsView(APIView):
  pass
