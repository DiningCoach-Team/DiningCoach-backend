from django.urls import path

from user.views import (
  UserSignUpView, UserLoginView, UserLogoutView, CustomizedTokenRefreshView,
  KakaoSignInView, GoogleSignInView, AppleSignInView, NaverSignInView,
  UserProfileView, UserHealthView, ConsentTermsView
)

from rest_framework_simplejwt.views import (
  TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

urlpatterns = [
  path('account/signup/', UserSignUpView.as_view()),
  path('account/login/', UserLoginView.as_view()),
  path('account/logout/', UserLogoutView.as_view()),
  path('account/token/refresh/', CustomizedTokenRefreshView.as_view()),

  path('auth/kakao/', KakaoSignInView.as_view()),
  path('auth/google/', GoogleSignInView.as_view()),
  path('auth/apple/', AppleSignInView.as_view()),
  path('auth/naver/', NaverSignInView.as_view()),

  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

  path('info/profile/', UserProfileView.as_view()),
  path('info/health/', UserHealthView.as_view()),
  path('info/consent/', ConsentTermsView.as_view()),
]
