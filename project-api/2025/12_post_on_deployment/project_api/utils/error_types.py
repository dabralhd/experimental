# error_types.py
from enum import Enum
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class ErrorType(Enum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    PRECONDITION_FAILED = 412
    GENERIC_CLIENT_ERROR = 400

# Example usage
def client_side_error(error_type: ErrorType) -> int:
    if error_type == ErrorType.BAD_REQUEST:
        logger.error('Bad Request')
        return ErrorType.BAD_REQUEST.value    
    elif error_type == ErrorType.UNAUTHORIZED:
        logger.error('Unauthorized')
        return ErrorType.UNAUTHORIZED.value     
    elif error_type == ErrorType.PAYMENT_REQUIRED:
        logger.error('Payment Required')
        return ErrorType.PAYMENT_REQUIRED.value 
    elif error_type == ErrorType.FORBIDDEN:
        logger.error('Forbidden')
        return ErrorType.FORBIDDEN.value 
    elif error_type == ErrorType.NOT_FOUND:
        logger.error('Not Found')
        return ErrorType.NOT_FOUND.value 
    elif error_type == ErrorType.METHOD_NOT_ALLOWED:
        logger.error('Method Not Allowed')
        return ErrorType.METHOD_NOT_ALLOWED.value 
    elif error_type == ErrorType.PROXY_AUTHENTICATION_REQUIRED:
        logger.error('Proxy Authentication')
        return ErrorType.PROXY_AUTHENTICATION_REQUIRED.value 
    elif error_type == ErrorType.REQUEST_TIMEOUT:
        logger.error('Request Timeout')
        return ErrorType.REQUEST_TIMEOUT.value 
    elif error_type == ErrorType.CONFLICT:
        logger.error('Conflict')
        return ErrorType.CONFLICT.value 
    elif error_type == ErrorType.PRECONDITION_FAILED:
        logger.error('Precondition Failed')
        return ErrorType.PRECONDITION_FAILED.value 
    
    logger.error('placeholder error')
    return ErrorType.GENERIC_CLIENT_ERROR.value 

