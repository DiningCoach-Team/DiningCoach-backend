from django.shortcuts import get_object_or_404

from user.models import User, UserProfile, UserHealth
from user.serializers.info_serializers import (
  UserBasicRetrieveSerializer, UserProfileRetrieveSerializer, UserHealthRetrieveSerializer,
  UserBasicUpdateSerializer, UserProfileUpdateSerializer, UserHealthUpdateSerializer,
)

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserAbstractView(RetrieveUpdateAPIView):
  serializer_class = None
  permission_classes = [IsAuthenticated]

  queryset = None
  serializer_classes = {'GET': None, 'PUT': None}
  lookup_field = None

  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def get(self, request, *args, **kwargs):
    self.serializer_class = self.serializer_classes['GET']
    self.kwargs[self.lookup_field] = self.request.user.id
    return super().retrieve(request, *args, **kwargs)

  @swagger_auto_schema(
    manual_parameters=[openapi.Parameter(name='Authorization', in_=openapi.IN_HEADER, description='Access Token', type=openapi.TYPE_STRING)]
  )
  def put(self, request, *args, **kwargs):
    self.serializer_class = self.serializer_classes['PUT']
    self.kwargs[self.lookup_field] = self.request.user.id
    return super().update(request, *args, **kwargs)

  @swagger_auto_schema(auto_schema=None)
  def patch(self, request, *args, **kwargs):
    raise MethodNotAllowed(method='PATCH', detail='GET 또는 PUT 메서드 요청만 처리할 수 있습니다. (PATCH 요청 처리 불가)')


# GET, PUT 'api/user/info/basic/'
class UserBasicView(UserAbstractView):
  queryset = User.objects.all()
  serializer_classes = {'GET': UserBasicRetrieveSerializer, 'PUT': UserBasicUpdateSerializer}
  lookup_field = 'id'


# GET, PUT 'api/user/info/profile/'
class UserProfileView(UserAbstractView):
  queryset = UserProfile.objects.all()
  serializer_classes = {'GET': UserProfileRetrieveSerializer, 'PUT': UserProfileUpdateSerializer}
  lookup_field = 'user_id'

  '''
  def get_object(self):
    queryset = self.filter_queryset(self.get_queryset())
  
    filter_kwargs = {'id': self.request.user.id}
    obj = get_object_or_404(queryset, **filter_kwargs)
  
    # May raise a permission denied
    self.check_object_permissions(self.request, obj)
  
    return obj
  '''


# GET, PUT 'api/user/info/health/'
class UserHealthView(UserAbstractView):
  queryset = UserHealth.objects.all()
  serializer_classes = {'GET': UserHealthRetrieveSerializer, 'PUT': UserHealthUpdateSerializer}
  lookup_field = 'user_id'


# GET, PUT 'api/user/info/consent/'
class ConsentTermsView(APIView):
  pass
