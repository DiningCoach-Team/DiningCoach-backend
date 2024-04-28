from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)
  error_res = {}

  if response is not None:
    try:
      error_res['error_message'] = response.data['detail']
    except KeyError:
      error_res['error_message'] = ('UNKNOWN_ERROR', str(response.data))

    error_res['error_code'] = response.status_code
    error_res['error_time'] = datetime.now()

    return Response(error_res, status=error_res['error_code'])

  return response


class CustomResponseRenderer(JSONRenderer):
  def render(self, data, accepted_media_type=None, renderer_context=None):
    response_data = renderer_context.get('response')
    response = {
      'status_code': response_data.status_code,
      'status_message': response_data.status_text,
      'data': data,
    }
    return super().render(response, accepted_media_type, renderer_context)
