# coding: utf-8

"""
@author: 武明辉 
@time: 2018/5/16 18:58
"""
import time
from functools import wraps


def time_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

if __name__ == '__main__':
    pass
