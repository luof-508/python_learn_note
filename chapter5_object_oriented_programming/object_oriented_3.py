#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/12
@File: object_oriented_3.py
"""


class MyClass1:
    def foo(self):
        print('foo')

    def bar():
        print('bar')


class MyClass2:
    xxx = 'XXX'
    def foo(self):
        print('foo')

    @classmethod
    def clsmtd(cls):
        print('{}.xxx={}'.format(cls.__name__, cls.xxx))


if __name__ == '__main__':
    # 示例1
    # a = MyClass1()
    # a.foo()
    # MyClass1.bar()
    # print(MyClass1.__dict__)
    # a.bar()
    # 示例2
    MyClass2.clsmtd()


