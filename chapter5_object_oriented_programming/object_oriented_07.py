#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/19
@File: object_oriented_07.py
十一、 继承
人类Person和猫类Cat都继承自动物类Animal
个体继承自父母，继承了父母的一部分特征，但也可以有自己的个性。
在面向对象的世界中，从父类继承，就可以直接拥有父类的属性和方法，这样可以减少代码、多复用。子类可以定义自己的属性和方法。
继承：Class SubClassName(FatherClassName)，这种形式就是从父类继承，括号中写上继承的类的列表。
继承可以让子类从父类获取特征（属性和方法）

父类：又称基类、base类、超类
子类：又称派生类
定义：Class子类名(基类1[,基类2,...])；如果没有后基类列表，等同于继承自object类。python3中object类是所以对象的根基类
继承的特殊属性和方法：
    __base__：类的基类
    __bases__：类的基类元组，实例无此属性
    __mro__：显示方法查找顺序，返回基类的元组
    mro()：同__mro__, __mro__就是mro的返回值，但是mro()是一个列表
    __subclasses__(): 所有子类列表

结论：
-从猫的实例c的属性字典`__dict__`和Animal类的属性字典可以看出，继承符合私有属性的定义。类中以`__`双下划线开头的属性，属于私有成员，python
解释器会自动将其重命名为`_类名__属性名`。实例属性`self.__age`是在Animal类中声明的，所以解释器将其重命名为`_Animal__age`；而Cat类继承
自Animal类，实例属性和类属性依然遵从私有属性的规则。
-类的属性只保存一份到`__dict__`中；子类的
`__dict__`不会保存继承自父类的属性，需要的时候从父类找就可以了，例如`c.__class__.__mro__；
子类的`__dict__`仅保存子类新增的属性
-继承时，公有的，子类、实例都可以访问；而私有成员被隐藏，子类和实例不可以直接访问，例如：
执行`c.cat__sleep()`时报`AttributeError： 'Cat` object has no attribute '_Cat__.age'`错误，只有私有变量`self.__age`所在类的
方法才可以访问这个私有变量。
-Garfield类重写了初始化方法`__init__`，因此Garfield类为继承父类的实例属性，只有重写的一个属性`{'name':'jinmao'}`
-属性的查找顺序：实例的`__dict__` ->类的`__dict__` -> 父类的`__dict__`，先找到立即返回，一直找到object类未找到抛异常。


"""


class Animal:
    HEIGHT = 0
    __COUNT = 0

    def __init__(self, age, weight, height):
        self.__age = age
        self.__weight = weight
        self.HEIGHT = height

    @classmethod
    def shout_count1(cls):
        print(cls.__COUNT)

    def __get_weight(self):
        print(self.__weight)

    def eat(self):
        print('{} eat'.format(self.__class__.__name__))


class Garfield(Animal):
    NAME = 'Garfield'

    def get_age(self):
        print(self.__age)


class Dog(Animal):
    def __init__(self, name):
        self.__name = name


if __name__ == '__main__':
    cat = Garfield(3, 5, 15)
    dog = Dog('dog')
    print(cat.HEIGHT)
    print(Garfield.__bases__)
    print(Animal.__dict__)
    print(Garfield.__dict__)
    print(cat.__dict__)
    print(dog.__dict__)
    print(cat.__class__.__mro__)
    print(cat.__class__.__dict__)
    print(Animal.__subclasses__())
    # print(cat.__COUNT)
    # print(cat.__get_weight)
    cat.shout_count1()
    cat.get_age()

