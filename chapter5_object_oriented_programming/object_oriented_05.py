#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: object_oriented_05.py
"""


class Person:
    def __init__(self, name):
        self._name = name  # 保护变量，内部函数或内部变量，不要引用
        self.__age = 18  # 私有属性

    def age_up(self, num: int):
        if 0 < self.__age < 150:
            self.__age += num

    def get_age(self):
        return self.__age

    def __growup(self, incr=1):
        if 0 < incr < 150:
            self.__age += incr


if __name__ == '__main__':

    tom = Person('tom')
    # print(tom.__dict__)
    # print(tom._Person__age)
    # tom._Person__age = 180
    # tom.__age = 100
    # print(tom.__dict__)
    # tom._name = 'jerry'
    # print(tom.__dict__)
    # 私有方法
    tom._Person__growup()
    print(tom.__dict__)
    print(tom.__class__.__dict__)


