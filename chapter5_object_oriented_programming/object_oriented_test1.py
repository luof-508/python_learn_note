#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/22
@File: object_oriented_test1.py
Mixin练习
Shape基类，要求所有子类都提供面积的计算，子类三角形、矩形、圆。

分析：
    计算圆面积，提供给用户的约方便越好，连括号都不想要，因此，设计成property比较好

    对于未实现的基类，最好raise otImplementedError，这是一种设计方法

    总结序列化对象的过程。

"""
import math
import json
import msgpack


class Shape:
    @property
    def calculate_area(self):
        raise NotImplementedError('Base Class not implemented')


def serialization_data(cls, method='json'):
    """对圆类实现序列化功能
    :param cls:
    :param method: 支持json、msgpack
    :return:
    """
    # todo 回顾对象的序列化过程。为什么序列化的是实例的__dict__，而不是对象
    if method == 'json':
        cls.serialization_data = lambda self: json.dumps(self.__dict__)
    elif method == 'msgpack':
        cls.serialization_data = lambda self: msgpack.dumps(self.__dict__)
    else:
        raise NotImplementedError('not implement serialization')
    return cls


@serialization_data
class Cycle(Shape):
    def __init__(self, radius):
        self.radius = radius

    @property
    def calculate_area(self):
        return math.pi * self.radius**2


class CalcuTriangleAreaMixin:
    def __init__(self, length, height):
        self.length = length
        self.height = height

    @property
    def calculate_area(self):
        return self.length * self.height / 2


class Triangle(CalcuTriangleAreaMixin, Shape):
    def __init__(self, length, height):
        super(Triangle, self).__init__()
        self.length = length
        self.height = height


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    @property
    def calculate_area(self):
        return self.length * self.width


if __name__ == '__main__':
    pass
