import functools
import time


def retry(logger, exc_to_check, tries: int = 5, delay: int = 3):
    def deco_retry(func):
        @functools.wraps(func)
        def func_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return func(*args, *kwargs)
                except exc_to_check as e:
                    logger.warn(f'Retrying in {mdelay} seconds: {type(e)}')
                    time.sleep(mdelay)
                    mtries -= 1
            return func(*args, **kwargs)
        return func_retry
    return deco_retry
