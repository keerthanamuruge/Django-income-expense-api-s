from rest_framework.views import exception_handler
import logging
logger = logging.getLogger(__name__)

handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    handlers = {
        'ValidationError': _handle_generic_error,
        'AuthenticationFailed': _handle_authentication_error,
        'PermissionDenied': _handle_generic_error,
    }
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__

    if response is not None:
        if exception_class in handlers:
            handlers[exception_class](exc, context, response)
            return response
        response.data = {
            "error": exc.default_detail,
            "code": exc.default_code
        }
    logger.exception(exc)
    return response

def _handle_generic_error(exception, context, response):
    response.data = {"error": exception.detail}
    logger.warning(exception)
    return response.data

def _handle_authentication_error(exception, context, response):
    response.data = {"error": "please login to continue"}
    logger.warning(exception)
    return response.data

