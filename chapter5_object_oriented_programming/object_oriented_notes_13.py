#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/5
@File: object_oriented_notes_13.py
八、`@contextlib.contextmanager`装饰器：
对于只生成器函数，且只yield 1个值时，可使用contextmanager装饰器，实现上下文管理，将yield返回值与as子句后面的变量绑定，并执行完yield后面的函数语句

`@functools.total_ordering`装饰器：
比较运算符`<、>、<=、>=`如果每一个都在类中实现太麻烦了，通过total＿ordering装饰器，只需要在类中实现`<、>、<=、>=`中的任意一个，即可进行实例的相关比较。
注意`==`必须单独实现，否则比较结果不准确
注释`__eq__`，可以看到`a1==a2`返回值为false。这与前述去重吻合：当没有给出`__eq__`时，判断例是否相等，默认比较内存中的id。
"""
import contextlib
import functools


@contextlib.contextmanager  # 不使用此装饰器时，不会执行exit函数语句
def foo():
    print('enter')
    yield 123
    print('exit')  # 异常情况，不能保证exit语句执行，使用try...finally语句


def foo1():
    print('enter')
    try:
        yield 123
    finally:
        print('exit')


@contextlib.contextmanager
def foo2():
    for i in range(3):  # yield不止1个值时，将抛RuntimeError: generator didn't stop异常
        yield i


@functools.total_ordering
class A:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return self.x == other.x

    def __gt__(self, other):
        return self.x > other.x


if __name__ == '__main__':
    # next(foo())
    # with foo() as f:
    #     print(f)
    #
    # with foo2() as f:
    #     print(f)

    a1 = A(3)
    a2 = A(4)
    print(a1 == a2)
    print(a1 > a2)
    print(a1 <= a2)
