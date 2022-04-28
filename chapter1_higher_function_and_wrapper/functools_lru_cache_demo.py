# coding = utf-8
"""
functools模块总结

1、partial：偏函数，作用：将一个函数参数固定，返回一个新的函数，原函数功能不变
2、lru_cache:least recently used,缓存，通过一个字典缓存被装饰函数的调用和返回值
            lru_cache(maxsize=128, typed=True),当maxsize为2的幂时，lru效果最好，当typed设置为True时，不同类型的函数参数
            将单独缓存，例如：f(3)和f(3.0)将视为具有不同结果的不同调用
    lru_cache的应用：前提：执行时间很长，且要多次执行，同一参数输出绝对相同； 用空间换时间的场景，例如从数据库中取数据，可使用缓存，更快
    缺点：不支持缓存过期，不支持清除操作，不支持分布式缓存，是一个单机缓存
    缓存中很重要的概念：命中，如果设计一个缓存，但是无法命中，效果就很差

AOP：面向切面编程。避免代码耦合。对于某些公共函数，在需要增强的时候，运用AOP思想，通过装饰器实现功能增强，同时让调用者和被调用者解耦
装饰器是AOP思想的体现，装饰器的作用是不改变业务函数，实现功能增强，同时避免侵入式代码。主要运用场景：日志分析、监控、路由、参数检查、权限、设计等
"""

__author__ = 'fg.luo'

import datetime
import functools
import inspect
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fn = logging.Formatter('[{asctime}]-{name}-{levelname}-{message}', style='{')
ch = logging.StreamHandler()
ch.setFormatter(fn)
ch.setLevel(logging.INFO)
logger.addHandler(ch)


# partial实现逻辑
def _partial_origin(func, *args, **kwargs):
    def wrapper_func(*fargs, **fkwargs):
        wrap_kwargs = kwargs.copy()
        wrap_kwargs.update(fkwargs)
        return func(*args, *fargs, **wrap_kwargs)
    wrapper_func.func = func
    wrapper_func.args = args
    wrapper_func.kwargs = kwargs
    return wrapper_func


def add(x, y):
    return x + y


new_add = functools.partial(add, x=7)


@functools.lru_cache()
def fib(n):
    """
    应用缓存，实现空间换时间
    """
    if n == 1:
        return 1
    elif n == 2:
        return 2
    return fib(n-1) + fib(n-2)


'----------------------------实现缓存-------------------------------------------------'


def lru_cache_demo(duration=3):
    def _cache_demo(func):
        """
        实现缓存，功能：查找、保存、自动清除
        add(1,2)、add(1)、add(x=1,y=2)、add(y=2,x=1），实现以上四种输入都视为同一个key
        """
        cache_dic = {}

        def cache_procedure(*args, **kwargs):
            # 自动清除过期缓存
            clear_cache()
            # make key
            key = get_key(args, kwargs)
            # 获取返回值
            if cache_dic.get(key):
                return cache_dic[key]
            res = func(*args, **kwargs)
            # 更新缓存
            cache_dic[key] = res, datetime.datetime.now()
            return res

        def clear_cache():
            cur_time = datetime.datetime.now()
            cache_dic_copy = cache_dic.copy()
            for k, v in cache_dic_copy.items():
                if (cur_time - v[1]).total_seconds() > duration:
                    cache_dic.pop(k)

        def get_key(args, kwargs):
            """
            运用inspect.signature中的parameters对象，将函数形参保存在一个有序字典中。
            函数输入参数 positional参数在前,keyword参数在后
            """
            key = args + tuple(kwargs.values())
            parameter_lst = list(inspect.signature(func).parameters.items())[len(args):]
            used_default_args = dict()
            for k, v in parameter_lst:
                used_default_args[k] = v.default
            for k, _ in kwargs.__items():
                used_default_args.pop(k)
            if used_default_args:
                key += tuple(used_default_args.values())
            return tuple(sorted(key))

        return cache_procedure
    return _cache_demo


def check_time(threshold):
    def _check_time(func):
        def _check_time_wrapper(*args, **kwargs):
            start_point = datetime.datetime.now()
            res = func(*args, **kwargs)
            total_time = (datetime.datetime.now() - start_point).total_seconds()
            if total_time > threshold:
                logger.error('Used func, total time:{}'.format(total_time))
            else:
                logger.info('get value by cache, total time:{}'.format(total_time))
        return _check_time_wrapper
    return _check_time


@check_time(2)
@lru_cache_demo(2)
def add_func(x=1, y=2):
    time.sleep(2)
    return x + y


if __name__ == '__main__':
    # result = add(x=8, y=5)
    # logger.info('New add:{}'.format(result))
    # start = datetime.datetime.now()
    # fib_res = fib(55)
    # logger.info('fib res:{}, time:{}'.format(fib_res, (datetime.datetime.now() - start).total_seconds()))
    # add_func(1)
    # add_func(x=1)
    # add_func(1, y=2)
    # add_func(y=2, x=1)
    # time.sleep(2)
    add_func(1, 2)
