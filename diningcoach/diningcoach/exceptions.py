from datetime import datetime

from django.http import JsonResponse

from rest_framework import status


def custom_bad_request(request, exception, *args, **kwargs):
  error_res = {
    'error_message': ('BAD_REQUEST', '잘못된 형식의 요청입니다.'),
    'error_code': status.HTTP_400_BAD_REQUEST,
    'error_time': datetime.now(),
  }

  return JsonResponse(error_res, status=error_res['error_code'])
  # """
  # Generic 400 error handler.
  # """
  # data = {
  #     'error': 'Bad Request (400)'
  # }
  # return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def custom_permission_denied(request, exception, *args, **kwargs):
  error_res = {
    'error_message': ('PERMISSION_DENIED', '요청하신 페이지에 접근 권한이 없습니다.'),
    'error_code': status.HTTP_403_FORBIDDEN,
    'error_time': datetime.now(),
  }

  return JsonResponse(error_res, status=error_res['error_code'])


def custom_page_not_found(request, exception, *args, **kwargs):
  error_res = {
    'error_message': ('PAGE_NOT_FOUND', '요청하신 페이지를 찾을 수 없습니다.'),
    'error_code': status.HTTP_404_NOT_FOUND,
    'error_time': datetime.now(),
  }

  return JsonResponse(error_res, status=error_res['error_code'])


def custom_server_error(request, *args, **kwargs):
  error_res = {
    'error_message': ('SERVER_ERROR', '요청이 서버에서 정상적으로 처리되지 않았습니다.'),
    'error_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
    'error_time': datetime.now(),
  }

  return JsonResponse(error_res, status=error_res['error_code'])
  # """
  # Generic 500 error handler.
  # """
  # data = {
  #     'error': 'Server Error (500)'
  # }
  # return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
