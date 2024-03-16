from rest_framework.views import exception_handler
from rest_framework.response import Response
from datetime import datetime


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)
  error_res = {}

  if response is not None:
    try:
      error_res['error_message'] = response.data['detail']
    except KeyError:
      error_res['error_message'] = str(response.data)

    error_res['error_code'] = response.status_code
    error_res['error_time'] = datetime.now()

    return Response(error_res, status=error_res['error_code'])

  return response
