#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: exe_module.py
猴子补丁：Monkey Patch
在运行时，动态的修改实例对象的属性。
从外部来改，破坏了对象的封装，临时用用。
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
