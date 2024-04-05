from django.urls import path, include

from user.views.account_views import (
  AccountSignUpView, AccountLoginView, AccountLogoutView,
  AccountPasswordChangeView, AccountPasswordResetView, AccountPasswordResetConfirmView,
  UserSignUpView, UserLoginView, UserLogoutView, UserCustomizedTokenRefreshView
)
from user.views.platform_views import KakaoSignInView, GoogleSignInView, AppleSignInView, NaverSignInView
from user.views.info_views import UserBasicView, UserProfileView, UserHealthView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
  path('account/signup/', AccountSignUpView.as_view(), name='signup'),
  path('account/login/', AccountLoginView.as_view(), name='login'),
  path('account/logout/', AccountLogoutView.as_view(), name='logout'),
  path('account/password/change/', AccountPasswordChangeView.as_view(), name='password_change'),
  path('account/password/reset/', AccountPasswordResetView.as_view(), name='password_reset'),
  path('account/password/reset/confirm/<str:uidb64>/<str:token>/', AccountPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

  path('platform/kakao/', KakaoSignInView.as_view()),
  path('platform/google/', GoogleSignInView.as_view()),
  path('platform/apple/', AppleSignInView.as_view()),
  path('platform/naver/', NaverSignInView.as_view()),

  path('info/basic/', UserBasicView.as_view()),
  path('info/profile/', UserProfileView.as_view()),
  path('info/health/', UserHealthView.as_view()),

  # path('auth/', include('dj_rest_auth.urls')),
  # path('auth/registration/', include('dj_rest_auth.registration.urls')),
  # path('allauth/', include('allauth.urls')),
  # path('allauth/account/', include('allauth.account.urls')),
]

# dj-rest-auth
# 1) api/user/auth/password/reset/ [name='rest_password_reset']
# 2) api/user/auth/password/reset/confirm/ [name='rest_password_reset_confirm']
# 3) api/user/auth/login/ [name='rest_login']
# 4) api/user/auth/logout/ [name='rest_logout']
# 5) api/user/auth/user/ [name='rest_user_details']
# 6) api/user/auth/password/change/ [name='rest_password_change']
# 7) api/user/auth/registration/

# django-allauth
# 1) api/user/allauth/signup/ [name='account_signup']
# 2) api/user/allauth/login/ [name='account_login']
# 3) api/user/allauth/logout/ [name='account_logout']
# 4) api/user/allauth/reauthenticate/ [name='account_reauthenticate']
# 5) api/user/allauth/password/change/ [name='account_change_password']
# 6) api/user/allauth/password/set/ [name='account_set_password']
# 7) api/user/allauth/inactive/ [name='account_inactive']
# 8) api/user/allauth/email/ [name='account_email']
# 9) api/user/allauth/confirm-email/ [name='account_email_verification_sent']
# 10) api/user/allauth/^confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
# 11) api/user/allauth/password/reset/ [name='account_reset_password']
# 12) api/user/allauth/password/reset/done/ [name='account_reset_password_done']
# 13) api/user/allauth/^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
# 14) api/user/allauth/password/reset/key/done/ [name='account_reset_password_from_key_done']
# 15) api/user/allauth/social/
