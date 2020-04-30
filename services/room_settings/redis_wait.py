#!/usr/bin/env/python3

from time import sleep


def redis_wait(
    redis, key, time=15,
):
    sleep_time = 0.25
    tries = int(time / sleep_time)
    result = None
    for _ in range(tries):
        result = redis.get(key)
        if result:
            return result
        sleep(0.25)
    return result
