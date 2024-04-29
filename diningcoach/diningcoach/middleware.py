from logging import getLogger
from time import process_time_ns
from django.db import reset_queries, connection
from django.conf import settings
from rest_framework.response import Response


class MetricMiddleware:
  """
  Custom middleware to calculate the response time of each request
  and log the metrics
  """

  def __init__(self, get_response) -> None:
    self.get_response = get_response

  def __call__(self, request) -> Response:
    reset_queries()

    ##### Before #####
    start_queries = len(connection.queries)
    start_time = process_time_ns()

    ##### Get Response #####
    response = self.get_response(request)

    ##### After #####
    end_time = process_time_ns()
    end_queries = len(connection.queries)

    ##### Calculate stats #####
    total_queries = (end_queries - start_queries)
    total_time = (end_time - start_time) / (10 ** 9)

    ##### Log metrics #####
    logger = getLogger('django.request')
    logger.debug('====================')
    logger.debug(f'Request: {request.method} {request.path}')
    if settings.DEBUG:
      logger.debug(f'Number of queries: {total_queries}')
    logger.debug(f'Total time: {(total_time):.4f}s')
    logger.debug('====================')

    return response
