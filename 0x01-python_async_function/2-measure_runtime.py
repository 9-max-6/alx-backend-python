#!/usr/bin/env python3
"""module: function measure_time()
"""
import asyncio
wait_n = __import__('1-concurrent_coroutines').wait_n


async def measure_time(n: int, max_delay: float):
    """measures the total execution time for wait_n(n, max_delay),
    and returns total_time / n.
    Your function should return a float."""