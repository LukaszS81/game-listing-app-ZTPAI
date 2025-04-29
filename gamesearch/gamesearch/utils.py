# projekt_root/gamesearch/custom_exception.py

from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # najpierw domyślny DRF handler
    response = exception_handler(exc, context)

    if response is not None:
        detail = response.data.get('detail', response.data)

        # jeśli detail jest tekstem
        if isinstance(detail, str):
            error_message = detail
        else:
            error_message = detail  # np. walidacyjne pola

        return Response(
            {'error': error_message, 'status': response.status_code},
            status=response.status_code
        )

    return response
