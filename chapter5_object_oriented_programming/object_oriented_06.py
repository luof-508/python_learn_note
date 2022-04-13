#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: object_oriented_06.py
猴子补丁：Monkey Patch
在运行时，动态的修改实例对象的属性。
"""


class Person:
    def __init__(self, chinese, english, history):
        self.chinese = chinese
        self.english = english
        self.history = history

    def get_store(self):
        return self.chinese, self.english, self.history


def get_store(self):
    return dict(chi=self.chinese, eng=self.english, his=self.history)


if __name__ == '__main__':
    stu = Person(97, 98, 99)
    stu.get_store()
