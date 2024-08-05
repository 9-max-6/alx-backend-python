#!/usr/bin/env python3
"""module: function: wait_n
"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n, max_delay):
    """wait_n should return the list of all the delays
    (float values). The list of the delays should be in ascending
    order without using sort() because of concurrency.
    """
    comprehended_wait_times = await asyncio.gather(
        *tuple(map(lambda _: wait_random(max_delay), range(n)))
    )

    return sorted(comprehended_wait_times)
