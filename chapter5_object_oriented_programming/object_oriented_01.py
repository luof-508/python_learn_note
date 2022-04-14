#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/10
@File: object_oriented_01.py
一、类定义和类的实例化

二、类属性和实例属性
"""


class Person(object):
    """an example class"""
    x = 'abc'  # 类属性
    age = 2
    height = 160

    def __init__(self, name, age=18):
        # __init__()方法不能有返回值，也就是只能是None
        print('This is init')
        self.name = name
        self.y = age

    def __new__(cls, *args, **kwargs):
        # 创建对象的时候，python解释器首先会调用__new__方法为对象在内存中分配空间，并返回对象引用
        # python解释器获得对象的引用后，将引用作为第一个参数，传递给__init__方法
        # 重写__new__方法一定要return super().__new__(cls)
        # 否则python解释器得不到分配了空间的对象引用，就不会调用对象的初始化方法
        # 注意：__new__是一个静态方法，在调用时需要主动传递cls参数
        print('This is new')
        return super().__new__(cls)

    def foo(self):  # 类属性foo，也是方法
        # foo是类的方法，但是foo是一个标识符，只是标识符foo正好对应了这个函数实体，
        # 定义一个函数之后，这个函数标识符会对应到创建出来的函数对象上，类方法foo本质也是这样一个过程。
        return 'my Class'

    def show(self, x, y):
        print(self.name, self.x, x, y)
        self.y = x  # 修改实例属性
        Person.x = x  # 修改类属性


if __name__ == '__main__':
    tom = Person('Tom')  # 实例化、初始化
    jerry = Person('Jerry')
    # print(tom.foo)
    # print(tom.name, tom.age)
    # print(jerry.name, jerry.age)
    # print(Person.age)
    # Person.age = 30
    # print(Person.age, tom.age, jerry.age)
    # print('===' * 3)
    # print(tom.__dict__)
    # tom.age = 18
    # print(Person.age, tom.age, jerry.age)
    # print(tom.__dict__)
    # print('-----------class-------')
    # print(Person.__class__)
    # print(sorted(Person.__dict__.items()), end='\n\n')
    # print('------instance tom--------')
    # print(tom.__class__)
    # print(sorted(tom.__dict__.items()), end='\n\n')
    # print("------tom's class--------")
    # print(tom.__class__.__name__)
    # print(sorted(tom.__class__.__dict__.items()), end='\n\n')
    # print(tom.__name__)
    # print(tom.__name__)  # tom只是Person类的一个实例的引用，所有没有__name__
    # print(tom.__class__, tom.__dict__, tom.__class__.__qualname__)
    # print(isinstance(jerry, tom.__class__))
    # print(tom.__class__, tom.__class__.__name__)
    # print(tom.__dict__)
    # print(Person.__dict__, Person.__class__)
    Person.age = 30
    print(Person.age, tom.age, jerry.age)
    print(Person.height, tom.height, jerry.height)
    Person.height += 20
    print(Person.height, tom.height, jerry.height)
    tom.height += 20
    print(Person.height, tom.height, jerry.height)
    jerry.height = 168
    print(Person.height, tom.height, jerry.height)

