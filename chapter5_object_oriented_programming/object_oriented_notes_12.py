#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/29
@File: object_oriented_notes_12.py

七、上下文管理：`__enter__`，`__exit__`方法：
    文件10操作可以对文件对象使用上下文管理，使＿用with...as语法。python用很多魔术方法，将很类实现得较为复杂，但是使用者用着特别方便，比如可以把一个自定义类变成上下。
    `__enter__`：进入与对象相关的上下文。一个对象中该方法存在，则with语句会把该方法的返回值绑定到as子句中指定的变量上
    `__exit__`(self, exc_type, exc_val, exc_tb)：退出与对象相关的上下文。exc_type, exc_val, exc_tb是三个与异常相关的参数。
    exc_type：异常类型
    exc_val：异常的值
    exc_tb：异常的追踪信息traceback。
    如果上下文退出时没有异常，则这3个参数都为None；如果有异常，退出上下文同时抛出异常，`__exit__`如果return一个等效的True，则压制异常不会抛出。
    通过with开启一个上下文运行环境，可以在执行前进行一些预加载或预处理工作，执行后执行收尾的工作，方便且安全，哪怕是退出python环境，也会执行`__exit__`语句。

    上下文管理，也可以像装饰器一样，实现前后的功能增强；上下文管理前提是，必须写在一个类上，然后在实例上执行
    装饰器高级玩法：
    类装饰器，类装饰器借助`__call__`魔术方法
    注意区分类装饰器和装饰一个类。
    多个装饰器，通过装饰器的等价式，就知道多个装饰器的调用顺序了：aa=time_it(add) -> a=Add(aa)-> a.__enter__()-> a.__call__(1,2) -> a.__exit__()
    装饰器，把跟业务无关的函数都抽象出去，实现非侵入式编程风格。
    通过类装饰器+上下文管理，避免侵入式代码的同时，不需要多重装饰器，实现更加丰富的功能：通过方法的封装，在执行前进行预加载，比如连接数据库、网络客户端请求
    等等；执行后保证关闭，出问题保证清理工作。

    上下文应用场景：
    1．增强功能：在代码执行前后增加代码，以增强功能。类似装饰器的功能
    2．资源管理：打开了资源需要关闭，例如文件对象、网络连接、数据库连接等
    3．权限验证：在执行代码之前，做权限验证，在`__enter__`中处理
"""
import datetime
import functools
import sys
import time


class Point:
    def __init__(self):
        print('init')

    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')


class E:
    def __init__(self):
        print('init')

    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')


class Add:
    """
    This is Add class
    """
    def __init__(self, fn):
        self._fn = fn
        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        print('__call__ start')
        ret = self._fn(*args, **kwargs)
        print('__call__ end')
        return ret

    def __enter__(self):
        self.start = datetime.datetime.now()
        print('Context wrapper: __enter__, time={}'.format(self.start))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total = (datetime.datetime.now() - self.start).total_seconds()
        print('Context wrapper: __exit__, exit time={}'.format(self.total))


def time_it(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        """
        This is wrapper
        :param args:
        :param kwargs:
        :return:
        """
        start = datetime.datetime.now()
        print('wrapper start, time={}'.format(start))
        ret = fn(*args, **kwargs)
        print('ret={}'.format(ret))
        total = (datetime.datetime.now() - start).total_seconds()
        print('wrapper end, exe time={}'.format(total))
        return ret
    return wrapper


@Add
@time_it
def add(*args, **kwargs):
    """
    This is add function
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.5)
    return sum(args) + sum(kwargs.values())


if __name__ == '__main__':
    # p = Point()
    # with p as f:
    #     # sys.exit()  # 测试异常退出python环境，会不会执行__exit__
    #     print(f == p)
    #     print('with...as')
    #
    # with E() as f:
    #     raise Exception('This is exception.')
    #     print('test exception')
    # add(1, 2)
    # print(add.__doc__, type(add))
    with add as f:
        print('context ret={}'.format(f(2, 3)))
