import time
from typing import List


def wait_until_true(conditions):
    """
    A generator that takes one or more boolean valued callables to
    check against. Yields when all the conditions are true, otherwise times out.
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
    max_call_count = 61  # Corresponds to an estimated timeout of 60 seconds.

    for condition in conditions:
        while not condition:
            if call_count == max_call_count:
                raise ValueError('Timeout: An unknown exception occurred.')
            time.sleep(1)
            call_count += 1
    yield
