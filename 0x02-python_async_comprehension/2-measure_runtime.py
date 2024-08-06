#!/usr/bin/env python3

async_comprehension = __import__('1-async_comprehension').async_comprehension
import asyncio
import time


async def measure_runtime() -> float:
    """a function to measure the runtime of four coroutines
    all async_comprehension() tasks
    """
    now = time.perf_counter()
    await asyncio.gather(async_comprehension(),
                   async_comprehension(),
                   async_comprehension(),
                   async_comprehension()
                   )
    after = time.perf_counter()

    return after - now
