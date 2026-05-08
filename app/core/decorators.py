import time

from functools import wraps

from app.core.logger import logger


def log_execution(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start_time = time.time()

        logger.info(
            f"Executing: {func.__name__}"
        )

        try:

            result = func(*args, **kwargs)

            execution_time = (
                time.time() - start_time
            )

            logger.info(
                f"Completed: {func.__name__} "
                f"in {execution_time:.2f}s"
            )

            return result

        except Exception as e:

            logger.exception(
                f"Error in {func.__name__}: {str(e)}"
            )

            raise e

    return wrapper
