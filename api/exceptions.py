from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    # Now add the HTTP status code to the response
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['detail'] = response.data.get('detail', 'An error occurred.')

    else:
        response = Response(
            {'error': 'An unexpected error occurred.', 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
