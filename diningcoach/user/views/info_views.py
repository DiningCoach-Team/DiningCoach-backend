from django.shortcuts import get_object_or_404

from user.models import User
from user.serializers.info_serializers import UserProfileRetrieveSerializer

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# GET 'api/user/info/basic/'
class UserBasicView(APIView):
  pass


# GET 'api/user/info/profile/'
class UserProfileView(RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserProfileRetrieveSerializer
  permission_classes = [IsAuthenticated]
  lookup_field = 'id'

  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def retrieve(self, request, *args, **kwargs):
    self.kwargs['id'] = self.request.user.id
    return super().retrieve(request, *args, **kwargs)

  # def get_object(self):
  #   queryset = self.filter_queryset(self.get_queryset())
  #
  #   filter_kwargs = {'id': self.request.user.id}
  #   obj = get_object_or_404(queryset, **filter_kwargs)
  #
  #   # May raise a permission denied
  #   self.check_object_permissions(self.request, obj)
  #
  #   return obj


# GET 'api/user/info/health/'
class UserHealthView(APIView):
  pass


# PATCH 'api/user/info/consent/'
class ConsentTermsView(APIView):
  pass
