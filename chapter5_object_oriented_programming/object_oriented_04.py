#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: object_oriented_04.py
方法调用
类不能调用普通方法，因为普通方法第一个参数必须是类的实例。
实例可以调用类中定义的所有方法；普通方法传入实例本身作为第一个参数， 静态方法和类方法本质是先调用__class__找到类，再调用方法；
`normal_mtd()`虽无语法错误，但不允许在类中这样定义。
"""


class Person:
    def normal_mtd():
        # 虽然无语法问题，但是不要这样写，使用静态方法代替
        print('normal')

    def mtd(self):
        print("{}'s method".format(self))

    @classmethod
    def class_mtd(cls):
        print('class = {0.__name__} ({0})'.format(cls))
        cls.HEIGHT = 170

    @staticmethod
    def static_mtd():
        print(Person.HEIGHT)


if __name__ == '__main__':
    # 类调用
    print('类调用')
    print(1, Person.normal_mtd())  # 虽然无语法问题，但是不要这样写，使用静态方法代替
    # print(2, Person.mtd())  # 调用普通方法
    print(3, Person.class_mtd())  # 调用类方法
    print(4, Person.static_mtd())  # 调用静态方法
    # 实例调用
    print('实例调用')
    tom = Person()
    # print(5, tom.normal_mtd())
    print(6, tom.mtd())  # 调用普通方法
    print(7, tom.class_mtd(), tom.__class__.class_mtd())  # 调用类方法  tom.mtd()等价于tom.__class__.class_mtd()
    print(8, tom.static_mtd(), tom.__class__.static_mtd())  # 调用静态方法  tom.mtd()等价于tom.__class__.static_mtd()
