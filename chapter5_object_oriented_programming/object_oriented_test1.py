#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/22
@File: object_oriented_test1.py
Mixin练习
Shape基类，要求所有子类都提供面积的计算，子类三角形、矩形、圆。
"""
import math


class Shape:
    def calculate_area(self, *args):
        pass


def calculate_cycle_area(cls):
    cls.calculate_area = lambda self: math.pi * self.radius**2
    return cls


@calculate_cycle_area
class Cycle(Shape):
    def __init__(self, radius):
        self.radius = radius


class CalTriangleArea:
    def calculate_area(self, length, height):
        return length * height / 2


class Triangle(CalTriangleArea, Shape):
    def __init__(self, length, height):
        self.length = length
        self.height = height


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width


if __name__ == '__main__':
    pass
