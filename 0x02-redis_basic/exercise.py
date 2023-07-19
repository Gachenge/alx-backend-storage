#!/usr/bin/env python3
"""
create a cache class in the __init__ method store instance of the redis
a private variable named _redis
"""
import redis
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """return a collable"""
    key = method.__qualname__

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """wrapper for decorated to count"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapped


def call_history(method: Callable) -> Callable:
    """store history"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """uses a list to store history"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """replays the history"""
    red = redis.Redis()
    func = fn.__qualname__
    count = red.get(func)
    count = int(count.decode("utf-8")) if count else 0
    print(f"{func} was called {count} times:")
    history = red.lrange(fn.__qualname__ + ":inputs", 0, -1)
    out = red.lrange(fn.__qualname__ + ":outputs", 0, -1)
    for input, output in zip(history, out):
        ins = input.decode('utf-8') if input else ""
        outs = output.decode('utf-8') if output else ""
        print(f"{func}(*{ins}) -> {outs}")


class Cache:
    """redis is a cache for storage"""

    def __init__(self):
        """instance of the redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate key and save to redis"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] =
            None) -> Union[str, int, bytes, float]:
        """callable to convert the data back to desired format"""
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """covert to string"""
        value = self._redis.get(key)
        return value.decode('utf-8') if value else None

    def get_int(self, key: str) -> int:
        """convert to int"""
        value = self._redis.get(key)
        return int(value.decode('utf-8')) if value else 0
