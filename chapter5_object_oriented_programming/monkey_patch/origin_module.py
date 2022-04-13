#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: origin_module.py
"""


class Person:
    def __init__(self, chinese, english, history):
        self.chinese = chinese
        self.english = english
        self.history = history

    def get_store(self):
        return self.chinese, self.english, self.history


if __name__ == '__main__':
    stu = Person(97, 98, 99)
    stu.get_store()

