#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/5
@File: object_oriented_notes_15.py
反射相关的魔术方法：`__getattr__、__setattr__、__hasattr__`:
|`__getattr__`|当通过搜索实例、实例的类及祖先类查找不到属性时，就会调用此方法；如果没有这个方法，就会抛AttributeError异常
|`__setattr__`|通过`obj.x`行增加、修改实例的属性都要调用`__setattr__`，包括初始化函数中的实例属性赋值
|`__delattr__`|通过实例来删除属性时调用此方法
|`__getattribute__`|实例所有的属性调用都从这个方法开始

属性的查找顺序：实例调用`__getattribute__() -> instance.__dict__ -> instance.__class__.__dict__ -> 继承的祖先类的__dict__ ->调用__getattr__()`
"""
import zipfile


class Base:
    n = 0


class Point(Base):
    z = 6

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getattr__(self, item):
        return 'missing {}'.format(item)

    def __setattr__(self, key, value):
        print('setattr')
        self.__dict__[key] = value

    def __delattr__(self, item):
        print('can not delete {}'.format(item))


class P:
    Z = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __delattr__(self, item):
        print('can not delete {}'.format(item))


class C(Base):
    C = 8

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getattr__(self, item):
        return 'missing {}'.format(item)

    def __getattribute__(self, item):
        # raise AttributeError
        return 'getattribute:{}'.format(item)


if __name__ == '__main__':
    # p1 = Point(1, 2)
    # print(p1.x)
    # print(p1.z)
    # print(p1.n)
    # print(p1.t)  # missing t
    # p2 = P(4, 5)
    # del p2.x
    # p2.z = 13
    # del p2.z
    # del p2.Z
    # print(p2.__dict__)
    # print(P.__dict__)
    # del P.Z
    # print(P.__dict__)

    c = C(3, 4)
    print(c.__dict__)
    print(c.x)
    print(c.c)
    print(c.n)
    print(C.__dict__)
    print(C.C)
