#!/usr/bin/env/python3

from time import sleep


def redis_wait(redis, key, time=10):
    sleep_time = 0.1
    tries = int(time / sleep_time)
    result = None
    for _ in range(tries):
        result = redis.get(key)
        if result:
            return result
        sleep(sleep_time)
    return result


__version__ = "0.0.1"
