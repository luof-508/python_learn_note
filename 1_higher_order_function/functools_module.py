"""
functools模块总结

1、partial：偏函数，作用：将一个函数参数固定，返回一个新的函数，原函数功能不变
2、lru_cache:least recently used,缓存，通过一个字典缓存被装饰函数的调用和返回值
            lru_cache(maxsize=128, typed=True),当maxsize为2的幂时，lru效果最好，当typed设置为True时，不同类型的函数参数
            将单独缓存，例如：f(3)和f(3.0)将视为具有不同结果的不同调用
    lru_cache的应用：前提：执行时间很长，且要多次执行，同一参数输出绝对相同； 用空间换时间的场景，例如从数据库中取数据，可使用缓存，更快
    缺点：不支持缓存过期，不支持清除操作，不支持分布式缓存，是一个单机缓存
    缓存中很重要的概念：命中，如果设计一个缓存，但是无法命中，效果就很差
"""
import datetime
import functools
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
    应用换算，实现空间换时间
    :param n:
    :return:
    """
    if n == 1:
        return 1
    elif n == 2:
        return 2
    return fib(n-1) + fib(n-2)


def cache_demo(func):
    """
    实现缓存，功能：查找、保存、自动清除
    """
    cache_dic = {}

    def cache_wrap(*args, **kwargs):
        # 自动清除过期缓存
        cur_time = datetime.datetime.now()
        cache_dic_copy = cache_dic.copy()
        for k, v in cache_dic_copy.items():
            if (cur_time - v[1]).total_seconds() > 3:
                cache_dic.pop(k)
        # make key
        key = args + (tuple,)
        for param in sorted(kwargs.items()):
            key += param
        logger.info('cache dict:{}'.format(cache_dic))
        # 获取返回值
        if cache_dic.get(key):
            logger.info('get res by cache:{}'.format(cache_dic[key]))
            return cache_dic[key]
        res = func(*args, **kwargs)
        # 更新缓存
        cache_dic[key] = res, datetime.datetime.now()
        logger.info('get result by calculate: {}'.format(res))
        return res
    return cache_wrap


@cache_demo
def add_func(x=2, y=3):
    return x + y


if __name__ == '__main__':
    result = add(x=8, y=5)
    logger.info('New add:{}'.format(result))
    start = datetime.datetime.now()
    fib_res = fib(55)
    logger.info('fib res:{}, time:{}'.format(fib_res, (datetime.datetime.now() - start).total_seconds()))
    add_func()
    time.sleep(1)
    add_func()
    time.sleep(1)
    add_func(1)
    time.sleep(1)
    add_func(2)
    time.sleep(1)
    add_func(1)
