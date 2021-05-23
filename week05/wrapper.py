"""
装饰器

装饰器是一个函数
以函数作为形参
返回值必须是一个函数
可使用@functionname，简化调用
装饰器的作用是不改变业务函数，实现功能增强，同时避免侵入式代码
"""
import time
import datetime


def copy_properties(dst):
    def _properties(src):
        dst.__name__ = src.__name__
        dst.__doc__ = src.__doc__
        dst.__qualname__ = src.__qualname__
        return dst
    return _properties


def logger(func):
    @copy_properties(func)
    def wrapper(*args, **kwargs):
        """
        This is a wrapper
        :param args:
        :param kwargs:
        :return:
        """
        print("args = {}, kwargs = {}".format(args, kwargs))
        start = datetime.datetime.now()
        ret = func(*args, **kwargs)
        end = datetime.datetime.now() - start
        print("function {} took {}s.".format(func.__name__, end.total_seconds()))
        return ret
    return wrapper


@logger
def add(*args, **kwargs):
    """
    文档字符串,第一行概述；可通过特殊属性__doc__访问；help就是调用函数的文档字符串

    :param args:
    :param kwargs:
    :return: int
    """
    print("====call add====")
    time.sleep(2)
    return sum(args) + sum(kwargs.values())


print(add(1, 2, 3, x=4, y=5))
print(add.__doc__, add.__qualname__, add.__name__, help(add), sep='\n')
