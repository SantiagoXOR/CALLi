from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from typing import Callable, TypeVar, Any
import functools
import logging

T = TypeVar('T')
logger = logging.getLogger(__name__)

def with_retry(
    max_attempts: int = 3,
    base_wait: float = 1,
    max_wait: float = 10,
    exceptions: tuple = (Exception,)
) -> Callable:
    """Decorador para reintentos con backoff exponencial."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                @retry(
                    stop=stop_after_attempt(max_attempts),
                    wait=wait_exponential(multiplier=base_wait, max=max_wait),
                    retry=lambda e: isinstance(e, exceptions),
                    before_sleep=lambda retry_state: logger.warning(
                        f"Retrying {func.__name__} after error: {retry_state.outcome.exception()}"
                    )
                )
                async def retry_func():
                    return await func(*args, **kwargs)
                
                return await retry_func()
            except RetryError as e:
                logger.error(f"Max retries reached for {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator
