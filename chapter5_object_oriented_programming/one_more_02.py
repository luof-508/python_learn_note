#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/11
@File: one_more_02.py

未实现和未实现异常
NotImplemented： 是一个单值，是<class 'NotImplementedType'>的实例
NotImplementedError： 是一个异常类型

运算符重载中的反向方法：
双目运算符。


"""


class A:

    def show(self):
        print(type(NotImplemented))
        print(type(NotImplementedError))
        #  类设计中，未实现的父类属性，抛一个未实现异常更合适
        raise NotImplementedError


class B:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):
        print('B add')
        return self.x + other.x

    def __radd__(self, other):  # 反向方法，
        print('B radd')
        return self + other


class C:
    def __init__(self, x):
        self.x = x

    # def __add__(self, other):
    #     print('C add')


class BImprove:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):
        try:
            ret = self.x + other.x
        except AttributeError:
            try:
                ot = int(other)
            except Exception:
                ot = 0  # 根据实际需求，选择不抛异常或抛异常
            ret = self.x + ot
        return ret

    def __radd__(self, other):  # 反向方法
        print('B radd')
        return self + other

    def __rsub__(self, other):
        pass

    def __rmod__(self, other):
        pass


if __name__ == '__main__':
    b = B(4)
    c = C(5)
    print(b + c)
    # 双目运算符反向加法：对象实例c加号左边，当c的类C中未实现__add__时，解释器尝试调用实例b中的__add__，如果b中实现了__add__，就直接使用
    print(c + b)
    # print(1 + b)  # 报AttributeError: 'int' object has no attribute 'x'。为什么？
    # 实际上，其调用逻辑是：1是int类型，内部实现了__add__方法，但是1 + b，b是B类的实例，int类中实现的__add__无法识别这个实例的类型，于是返回
    # 了NotImplemented单值；解释器发现这是一个值（类似于c + b，从c中没有找到__add__，返回的是None单值）,于是继续发起对第二个对象b的__radd__
    # 方法的调用，对象b实现了__radd__，但数字1没有属性x，所以抛出了AttributeError异常。
    # 解决方案：使用异常捕获处理，类似于int返回NotImplemented。
    print('~~~~~~~~~~')
    b_im = BImprove(11)
    print(1 + b_im)
    print('abc' + b_im)
    print('5' + b_im)

