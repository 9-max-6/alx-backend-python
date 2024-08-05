#!/usr/bin/env python3
"""module: function task_wait_random()
"""
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random

def task_wait_random(max_delay: int) -> asyncio.Task:
    """A function to take an int max_delay and return
    an asyncio.Task
    """

    return asyncio.create_task(wait_random(max_delay))

