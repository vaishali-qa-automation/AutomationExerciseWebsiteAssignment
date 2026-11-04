import logging
import time
from collections.abc import Callable
from functools import wraps

logger = logging.getLogger(__name__)


def logging_decorator(func):
    """Log method execution and failures.

    Args:
        func: Function to decorate.

    Returns:
        The decorated function.
    """

    @wraps(func)
    def logging_wrapper(*args, **kwargs):
        visible_args = args[1:] if len(args) > 0 else args

        logger.debug(
            f"Executing {func.__name__} with agrs {visible_args} and kwargs {kwargs}"
        )

        try:
            result = func(*args, **kwargs)

            logger.debug(f"Successfully executed {func.__name__}")

            return result

        except Exception as e:
            logger.warning(
                f"Transient exception in '{func.__name__}': {type(e).__name__} -> {e}. "
            )
            raise

    return logging_wrapper


def retry_on_exception(
    times: int = 3,
    delay: float = 0.0,
    exceptions: tuple[type[BaseException], ...] = (
        Exception,
    ),  # Configurable exceptions
) -> Callable:
    """Decorator to retry a function when specified exceptions occur.

    Args:
        times: Maximum number of attempts.
        delay: Delay in seconds between retry attempts.
        exceptions: A tuple of exception classes to catch and retry on.
    """
    if times < 1:
        raise ValueError("times must be at least 1.")

    def retry_decorator(func: Callable) -> Callable:
        @wraps(func)
        def retry_wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times:
                        logger.exception(
                            f"Method '{func.__name__}' failed final attempt ({times}/{times})."
                        )
                        raise  # Re-raise the caught exception

                    logger.warning(
                        f"Method '{func.__name__}' failed on attempt {attempt}/{times}. "
                        f"Reason: {type(e).__name__}. Retrying in {delay}s..."
                    )

                    if delay > 0:
                        time.sleep(delay)

        return retry_wrapper

    return retry_decorator


def retry_on_condition(times: int = 3, delay: float = 0) -> Callable:
    """Retry a function when a specified condition occurs."""

    def retry_on_condition_decorator(func):
        @wraps(func)
        def retry_on_condition_wrapper(*args, **kwargs):
            result = False
            for attempt in range(1, times + 1):
                result = func(*args, **kwargs)
                if result:
                    break
                if delay:
                    time.sleep(delay)
            return result

        return retry_on_condition_wrapper

    return retry_on_condition_decorator
