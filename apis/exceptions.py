from rest_framework.views import exception_handler
from apis.utils.common import ServiceError
import logging

logger = logging.getLogger("color_logger")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request")

    if request:
        log_message = f"{request.method} {request.path} - Exception: {exc}"

        if isinstance(exc, ServiceError):
            log_message = f"{request.method} {request.path} - Custom Exception: {exc.error_message}"

        logger.error(log_message)

    if isinstance(exc, ServiceError) and response is not None:
        response.data = {
            "error": exc.error_message,
        }
        response.status_code = exc.status_code
    elif isinstance(exc, ServiceError):
        # fallback in case response is None
        from rest_framework.response import Response
        return Response(
            {"error": exc.error_message},
            status=exc.status_code
        )

    return response
