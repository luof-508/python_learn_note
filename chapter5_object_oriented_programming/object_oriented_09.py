#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/21
@File: object_oriented_09.py
"""


class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class B(A):
    def __init__(self, a, b):
        A.__init__(self, a+b, a-b)
        self.b = a
        self.c = b

    def printf(self):
        print(self.b)
        print(self.c)


class Animal:
    def __init__(self, age):
        self.__age = age

    def show(self):
        print(self.__age)


class Garfield(Animal):
    def __init__(self, age, weight):
        # 调用父类的__init__方法的顺序，决定了show方法的执行结果
        # 如果实例属性是私有成员，会发现，又有不一样的结果
        super(Garfield, self).__init__(age)
        self.age = age + 1
        # super(Garfield, self).__init__(age)

    def get_age(self, default=8):
        # 父类的初始化方法可以在子类的任何地方调用，调用位置不同可能引起不同结果，这一点一定要注意。
        super(Garfield, self).__init__(default)


if __name__ == '__main__':
    # f = B(2, 3)
    # print(f.__dict__)
    # print(f.__class__.__bases__)
    # f.printf()
    cat = Garfield(9, 5)
    cat.show()
    print(cat.__dict__)
