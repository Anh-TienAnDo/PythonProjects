import functools
import logging
import time

def logger(cls=None):
    def start(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if cls:
                logging.info("Class %s", cls)
            logging.info(f"Hàm {func.__name__} với args: {args}, kwargs: {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return start

def timer(cls=None):
    def start(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if cls:
                logging.info("Class %s", cls)
            logging.info(f"Hàm {func.__name__} chạy trong {end - start} giây")
            return result
        return wrapper
    return start
