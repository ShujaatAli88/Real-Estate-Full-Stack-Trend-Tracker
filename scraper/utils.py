from sentry_sdk import capture_exception

def log_exception(*, exception, message: str) -> None:
    """
    Log Custom Exceptions to the sentry

    example usage
    log_exception(exception=ValueError, message="This is Value Error")
    """

    exception_obj = exception(message)
    capture_exception(exception_obj)