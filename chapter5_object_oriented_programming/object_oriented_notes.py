#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/6
@File: object_oriented_notes.py

描述器：当类的定义中实现了`__get__、__set__、__delete__`三个魔术方法中的任意一个时，那么这个类就是一个描述器
当仅实现了`__get__`，称为非数据描述器non data descriptor;
当同时实现了`__get__` + `__set＿`或`__delete__`就是数据描述器data descriptor
如果一个类的类属性包含描述器，那么这个类称为owner属主
常用的描述器：property

当类A的实例x是类B的属性时，如果类A中给出了`__get__`方法，则对类B属性x的读取（不管是通过B的实例或B），或者进一步通过属性x访问类A的属性，将会触发`__get__`方法；
当类A的实例是类B的实例属性，通过类B的实例属性访问类A的实例的属性的时候，不会触发`__get__`方法
`__get___(self, instance, owner)`:
instance：属主的实例，当通过类B的实例b读取属性x时，解释器自动传入b和B
owner：属主，当通过类B读取属性x时，instance
为None，只传入B
对于数据描述器：当类D中的类属性x为数据描述器时，则对类D的实例d进行访问、修改属性x操作时（d.x或d.x=100），数据描述器的`__dict__`优先实例的`__dict__`
所以，一但类属性x为数据描述器，则实例b只能操作类属性x，无标识符为x的实例属性；而操作类属性x又受描述器控制，才会有d.x=100时触发了数据描述器的`__set__`方法，有点像运算符重载`d.x=100 -> d.x.__set__(d, 100)`。
本质上：数据描述器`d.x=100 -> d.__getattribute__ -> d.x.__set__`，还没有走到写`d.__dict__`的操作，所以操作d.x的时候，从自己的`__dict__`中找不到x，就找类的，而类属性x又是一个描述器，进而触发了`__get__`.
python的方法都实现为非数据描述器（例如staticmethod、classmethod），因此实例可以重新 定义和覆盖方法，这允许单个实例可以获取与同一类的其他实例不同的行为。
property函数实现为一个数据描述器，因此实例不
能覆盖属性的行为

"""


class A:
    AA = 'aa'

    def __init__(self):
        print('A.init')
        self.a1 = 'a1'

    def __get__(self, instance, owner):
        print('A:__get__', self, instance, owner)
        return self  # 通常return self


class B:
    x = A()

    def __init__(self):
        print('B.init')
        # self.x = 100
        self.y = A()


class C:
    CC = 'cc'

    def __init__(self):
        print('C.init')
        self.c1 = 'c1'

    def __get__(self, instance, owner):
        print('C:__get__', self, instance, owner)
        return self  # 通常return self

    def __set__(self, instance, value):
        print('C:__set__', self, instance, value)


class D:
    x = C()

    def __init__(self):
        print('D.init')
        self.x = 100
        self.y = 123


class E:

    @classmethod
    def foo(cls):
        pass

    @staticmethod
    def bar():
        pass

    @property
    def z(self):
        return 2

    def __init__(self):
        self.foo = 100  # foo和、bar方法都为非数据描述器，所以可以直接赋值修改
        self.bar = 123
        self.z = 'z'  # z方法为数据描述器，不能在实例中替换


if __name__ == '__main__':
    print(B.x)
    print(B.x.AA)  # 通过类B读取类属性x，因为x是一个描述器，触发__get__
    print('~~~~~~~~~~')
    b = B()
    print(b.x.AA)  # 通过类B的实例b读取类属性x，因为x是一个描述器，触发__get__
    print('~~~~~~~~~~')
    print(b.y.a1)  # 通过实例属性访问类A的实例的属性，不会触发__get__

    print('-----------')
    print(D.x)
    d = D()
    print(d.__dict__)  # 查看实例d的__dict__是否有属性x
    print(D.__dict__)
    print('~~~~~~~~~~~~~~')
    print(d.x)
    d.x = 100    # 尝试为实例d增加属性x
    print(d.x)   # 查看‘赋值即定义’是否可以增加实例属性x。从结果可以看出，由于类属性x是数据描述器，由于受数据描述器拦截，无法给实例d的__dict__写入x,即增加x属性。
    print(d.__dict__)
    print('~~~~~~~~~~~~~')
