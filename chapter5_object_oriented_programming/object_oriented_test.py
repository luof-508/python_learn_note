#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/15
@File: object_oriented_test.py
面向对象，如何设计类：

1、随机整数生成，可以指定一批生成的个数，可以指定数值的范围，可以调整每批生成数字的个数。
    one more:使用此类，随机生成20个数字，两两配对，形成二维坐标系的坐标，把这些坐标组织起来，并打印输出


面向对象要解耦，结构化编程、模块化编程，每一个方法实现一个单一功能

"""
import secrets


# 1、生成随机整数
class RandomGenerator(object):
    """随机生成整数

    指定一批生成的个数，可以指定数值的范围，可以调整每批生成数字的个数。
    """
    def __init__(self, num=10, start=0, stop=99):
        """

        :param num: 指定生成整数的个数
        :param start: 指定生成整数的开始
        :param stop: 指定生成整数的结束
        """
        self.num = num
        self.start = start
        self.stop = stop
        self.rd = secrets.SystemRandom()
        self.g = self._generate(start, stop)

    def generator_int(self, num: int = None, start: int = None, stop: int = None):
        g = self._generate(start, stop) if start and stop else self.g
        if num:
            return [next(g) for _ in range(num)]
        return [next(g) for _ in range(self.num)]

    def _generate(self, start, stop):
        while True:
            yield self.rd.randint(start, stop)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """打印类的对象的时候，如果类中定义了__repr__属性，则print自动调用__repr__"""
        return '{}:{}'.format(self.x, self.y)

    def __str__(self):
        return '{}:{}'.format(self.x, self.y)


# 二、记录车辆信息，并实现车辆信息管理：增加车辆信息、显示全部车辆信息
class Car:
    """车辆信息"""
    def __init__(self, mark, color, price, speed):
        self.mark = mark
        self.color = color
        self.price = price
        self.speed = speed

    def add_car_attr(self, info):
        """增加车辆信息，车辆信息在车上，所以应该在车上"""
        pass


class CarInfo:
    """车辆管理"""
    lst = []

    def add_car(self, car: Car):
        """增加车，所有车在车辆管理上，所以add_car应该放到车辆管理上"""
        self.lst.append(car)

    def get_car_info(self):
        return self.lst  # 数据在哪儿，在哪儿处理，所有如果需要看所有车，应在此处处理

    def __repr__(self):
        pass


if __name__ == '__main__':
    rg = RandomGenerator()
    print(rg.generator_int())
    lst = [Point(*item) for item in zip(rg.generator_int(10), rg.generator_int(10))]
    # 打印方式一，使用__repr__属性
    print(lst)
    # 打印方式二
    for p in lst:
        print(p.x, p.y)
