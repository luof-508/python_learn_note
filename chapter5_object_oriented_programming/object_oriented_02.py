#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/12
@File: object_oriented_02.py

一、装饰一个类
    装饰一个类的作用：
    1. 对于写好的模块，某些特定的场景缺少一个方法或属性，但是又不便于修改已经写好的项目，可以通过装饰器外部引用，
       为这个类Class增加需要的属性或方法后，再使用。

    本质上是为类对象动态的添加一个属性。
"""


def set_name_property(name):
    def _wrapped(fn):
        print('wrapper {}'.format(fn))
        fn.NAME = name
        return fn
    return _wrapped


@set_name_property('My class')
class Person:
    age = 18

    def __init__(self, age, name):
        self.name = name
        self.age = age

    def __new__(cls, *args, **kwargs):
        print('this is new')
        return super().__new__(cls)

    def show(self):
        print(self.age, Person.age)


if __name__ == '__main__':
    tom = Person('tom', 20)
    print("tom name = {}, Person's name = {}, Person's age = {}".format(
        tom.name, tom.__class__.NAME, tom.__class__.__dict__['age']))
