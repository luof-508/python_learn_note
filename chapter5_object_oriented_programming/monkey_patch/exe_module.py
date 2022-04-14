#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: exe_module.py
猴子补丁：Monkey Patch
    在运行时对属性进行动态替换。就是把类添加、修改属性的过程，封装到某个函数、某个类、某个模块里。要么在对象的属性上替换，要么在类的属性上替换。

    外部修改，破坏了对象的封装，临时用用。
"""
from origin_module import Person
from patch_module import get_store


def monkey_patch_person():
    Person.get_store = get_store  # 打补丁,要么在对象的属性上替换，要么在类的属性上替换


if __name__ == '__main__':
    stu1 = Person(97, 98, 99)
    print(stu1.get_store())
    monkey_patch_person()
    stu = Person(97, 98, 99)
    print(stu.get_store())
