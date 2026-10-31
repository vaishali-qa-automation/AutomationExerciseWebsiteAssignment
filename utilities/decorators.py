import logging
import time
from functools import wraps
from typing import Callable

from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)


def logging_decorator(func) :
    """Log method execution and failures.

    Args:
        func: Function to decorate.

    Returns:
        The decorated function.
    """

    @wraps(func)
    def logging_wrapper(*args, **kwargs):
        logger.debug(
            f"Executing {func.__name__}"
        )

        try:
            result = func(*args, **kwargs)

            logger.debug(
                f"Successfully executed {func.__name__}"
            )


            return result

        except Exception:
            logger.exception(
                f"Exception occurred while executing {func.__name__}"
            )
            raise

    return logging_wrapper


def retry_on_exception(
    times: int = 3,
    delay: float = 0,
) -> Callable:
    """Retry a function when a specified exception occurs.

    Args:
        times: Maximum number of attempts.
        delay: Delay in seconds between retry attempts.

    Returns:
        A decorator that retries the decorated function.

    Raises:
        ValueError: If ``times`` is less than one.
    """
    if times < 1:
        raise ValueError("times must be at least 1.")

    def retry_decorator(func) :

        @wraps(func)
        def retry_wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)

                except [StaleElementReferenceException, TimeoutException, NoSuchElementException] as ex:
                    if attempt == times:
                        logger.exception(
                            f"{func.__name__} failed after {times} attempts."
                        )
                        raise ex

                    logger.warning(
                        f"{func.__name__} failed on attempt {attempt}/{times}. Retrying..."
                    )

                    if delay:
                        time.sleep(delay)
            return None

        return retry_wrapper

    return retry_decorator

def retry_on_condition(
    times: int = 3,
    delay: float = 0
) -> Callable:
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