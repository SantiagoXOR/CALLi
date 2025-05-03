import functools
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar, cast

from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

T = TypeVar("T")
logger = logging.getLogger(__name__)


def with_retry(
    max_attempts: int = 3,
    base_wait: float = 1,
    max_wait: float = 10,
    exceptions: tuple = (Exception,),
) -> Callable:
    """Decorador para reintentos con backoff exponencial."""

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:

                @retry(
                    stop=stop_after_attempt(max_attempts),
                    wait=wait_exponential(multiplier=base_wait, max=max_wait),
                    retry=lambda e: isinstance(e, exceptions),
                    before_sleep=lambda retry_state: logger.warning(
                        f"Retrying {func.__name__} after error: {retry_state.outcome.exception()}"
                    ),
                )
                async def retry_func():
                    return await func(*args, **kwargs)

                result = await retry_func()
                return cast(T, result)
            except RetryError as e:
                logger.error(f"Max retries reached for {func.__name__}: {e!s}")
                raise

        return wrapper

    return decorator
