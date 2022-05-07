#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/6
@File: object_oriented_11.py
"""
import functools
import inspect


class ClassMethod:
    def __init__(self, fn):
        print(fn)
        self._fn = fn

    def __get__(self, instance, owner):
        print(self, instance, owner)
        # return self._fn(owner)
        return functools.partial(self._fn, owner)


class StaticMethod:
    def __init__(self, fn):
        print(fn)
        self._fn = fn

    def __get__(self, instance, owner):
        print(self, instance, owner)
        return self._fn


class A:

    @StaticMethod
    def foo():
        print('static')

    @ClassMethod  # foo = ClassMethod(foo) -> 新的foo是类ClassMethod的实例， 而ClassMethod非数据描述器，故通过A.foo读取类属性foo时，触发调用__get__，而__get__返回的是固定了参数cls的新的foo。所有最后可以直接foo()执行函数。
    def bar(cls):
        print(cls.__name__)


if __name__ == '__main__':
    # f = A.foo
    # print(f)
    # f()
    b = A.bar
    print(b)
    b()
    inspect.signature()
    inspect.Signature
