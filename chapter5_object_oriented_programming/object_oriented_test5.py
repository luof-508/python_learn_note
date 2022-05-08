#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/8
@File: object_oriented_test5.py

# 同时存在反射和描述器会怎么样: __setattr__, __getattr__, __delattr__， __set__, __get__， __delete__

面向对象--魔术方法之高级玩法2：自定义Property类，实现类property功能

需求分析：property是一个数据描述器。从类A的属性name被装饰的流程推导：
    首先，`@property`装饰name -> 返回一个数据描述器property的实例，与标识符name绑定，原name方法成为property实例的一个动态属性；
    然后，`@name.setter`再次装饰第二个name，第一个name已经是property的实例了，装饰过后，第二个name方法再次成为property实例的第二个动态属性；
    最后，类A的name属性其实是被装饰两次后的一个数据描述器器，这个数据描述器被动态绑定了访问和修改实例属性`_name`的两个方法。

    所以，类A实例化后，通过`a.name`访问实例属性`_name`时，因为类属性name是一个数据描述器，自动触发`__get__`方法，`__get__`内部调用了动态绑定的访问实例属性`_name`的第一个name方法；
    而通过`a.name="Tom"`修改实例属性`_name`时，触发`__set__`方法，`__set__`内部一定调用了被动态绑定的修改实例属性`_name`的第二个name方法。

由上述分析，自定义一个Property数据描述器；初步实现property类的功能。

"""


class Property:
    def __init__(self, get_method):
        self.get_method = get_method
        self.set_method = None

    def __set__(self, instance, value):
        self.set_method(instance, value)

    def __get__(self, instance, owner):
        return self.get_method(instance)

    def setter(self, method):
        self.set_method = method
        return self


class A:
    def __init__(self, name, age):
        self._name = name
        self.__age = age

    @Property
    def age(self):
        print("I'm the Property")
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = value

    @property  # -> name=property(name)
    def name(self):
        print("I'm the property")
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        print('del name')
        del self._name


if __name__ == '__main__':
    a = A('Tom', 19)
    # print(a.__dict__, a.__class__.__dict__)
    # print(a.name)
    # a.name = 'hah'
    # print(a.name)
    # print(a.__dict__)
    # del a.name
    # print(a.__dict__)
    print('~~~~~~~~~自定义Property类测试~~~~~~~~~~~~~~~~')
    print(a.__dict__)
    print(a.age)
    a.age = 100
    print(a.age)
    print(a.__dict__)
