from rest_framework.response import Response


def api_response(
    *,
    status="success",
    message="Request successful",
    data=None,
    http_status=200,
):
    """
    Standardized API response for EnterpriseFlow.
    """

    return Response(
        {
            "status": status,
            "message": message,
            "data": data,
        },
        status=http_status,
    )


def success_response(
    message,
    data=None,
    http_status=200,
):
    return api_response(
        status="success",
        message=message,
        data=data,
        http_status=http_status,
    )


def error_response(
    message,
    data=None,
    http_status=400,
):
    return api_response(
        status="error",
        message=message,
        data=data,
        http_status=http_status,
    )
    