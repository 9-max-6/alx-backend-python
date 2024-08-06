#!/usr/bin/env python3
"""module: coroutine: measure_runtime
"""
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """a function to measure the runtime of four coroutines
    all async_comprehension() tasks
    """
    now = time.perf_counter()
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
        )
    after = time.perf_counter()

    return after - now
