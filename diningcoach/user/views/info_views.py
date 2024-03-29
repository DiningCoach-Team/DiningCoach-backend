from user.models import User
from user.serializers import UserProfileRetrieveSerializer

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


# api/user/info/profile/
class UserProfileView(RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserProfileRetrieveSerializer
  permission_classes = [IsAuthenticated]


# api/user/info/health/
class UserHealthView(APIView):
  pass


# api/user/info/consent/
class ConsentTermsView(APIView):
  pass
