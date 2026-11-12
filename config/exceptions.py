from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Centralized exception handler.

    Ensures DRF errors use the EnterpriseFlow response format.
    """

    response = exception_handler(exc, context)

    if response is None:
        return None

    message = "Request failed"

    if isinstance(response.data, dict):
        message = (
            response.data.get("detail")
            or response.data.get("message")
            or message
        )

    elif isinstance(response.data, list):
        message = "Validation failed"

    return Response(
        {
            "status": "error",
            "message": str(message),
            "data": response.data,
        },
        status=response.status_code,
    )