from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView


# api/user/platform/kakao/
class KakaoSignInView(APIView):
  pass


# api/user/platform/google/
class GoogleSignInView(APIView):
  pass


# api/user/platform/apple/
class AppleSignInView(APIView):
  pass


# api/user/platform/naver/
class NaverSignInView(APIView):
  pass
