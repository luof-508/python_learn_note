#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/12
@File: object_oriented_03.py
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


class Person:
    age = 18

    def get_age(self):
        return self.age

    @classmethod
    def class_method(cls):
        print("class = {0.__name__} ({0})".format(cls, cls))
        # 通过cls操作类属性
        cls.HEIGHT = 170
        print(cls().get_age())

    @staticmethod
    def static_method():
        print(Person.HEIGHT)



if __name__ == '__main__':
    # 示例1
    # a = MyClass1()
    # a.foo()
    # MyClass1.bar()
    # print(MyClass1.__dict__)
    # a.bar()
    # 示例2
    # MyClass2.clsmtd()
    Person.class_method()
    Person.static_method()
    print(Person.__dict__)

