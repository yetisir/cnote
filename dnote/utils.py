import sys
import functools
import contextlib
import os
import datetime


def cli_args(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if 'args' not in kwargs:
            return function(*args, **kwargs)

        if kwargs['args'] is None:
            kwargs['args'] = sys.argv[1:]
            return function(*args, **kwargs)

    return wrapper


@contextlib.contextmanager
def suppress_std(std_type):
    std = f'std{std_type}'
    save_std = getattr(sys, std)
    with open(os.devnull, 'w') as devnull:
        setattr(sys, std, devnull)
    yield
    setattr(sys, std, save_std)


def now():
    return datetime.datetime.utcnow()