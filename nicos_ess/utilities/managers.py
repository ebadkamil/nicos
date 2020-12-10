import time
from typing import List


def wait_until_true(conditions, max_call_count=61, sleep_duration=1):
    """
    A generator that takes one or more boolean valued callables to
    check against. Yields when all the conditions are true, otherwise times out.
    Here the maximum call count represents how many times a call should be made
    for the truth values of the given conditions. By default, the generator will
    time out in about 60 seconds.

    Note that with the current implementation, the conditions are evaluated
    serially. A parallel implementation can be done, if needed.
    """
    if not isinstance(conditions, List):
        raise TypeError('The argument should be a list.')
    for condition in conditions:
        if not isinstance(condition, bool):
            raise TypeError('The elements should be boolean valued.')
    if len(conditions) == 0:
        raise ValueError('There should be at least one condition to be'
                         'satisfied.')

    call_count = 1

    for condition in conditions:
        while not condition:
            if call_count == max_call_count:
                raise ValueError('Timeout: An unknown exception occurred.')
            time.sleep(sleep_duration)
            call_count += 1
    yield


def wait(wait_time=1):
    time.sleep(wait_time)
    yield
