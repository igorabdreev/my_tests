"""Custom exceptions for module "api" """
from requests.exceptions import RequestException


class UnavailableServiceError(RequestException):
    """Custom exception for error "max retries unknown host" """
    pass
