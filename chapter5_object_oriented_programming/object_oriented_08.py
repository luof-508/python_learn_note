#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/19
@File: object_oriented_08.py

十二、方法的重写、覆盖override：
    super方法，很方便的访问祖先类；静态方法、类方法、一般属性都可以被重写覆盖。
    子类Garfield实例cat调用继承自父类shout属性的调用，从执行结果`<class '__main__.Garfield'> Garfield shout`
    可以看出，虽然属性定义在父类， 但是cls由传入的参数决定，cls传入的是Garfield，所以打印的`__name__`是Garfield
    被重写的属性，在子类的`__dict__`就会保存这个属性，而继承的属性，只会保存在父类的`__dict__`中。

十三、继承中的初始化：
    B类继承自父类A，子类B中重写了__init__，好的习惯，则要调用一下父类A的__init__；因为子类的初始化__init__方法不会自动调用父类的__init__，
    如果子类中需要继承父类的属性，不调用，只有到运行节点抛异常了才会发现。
"""


class Animal:
    def __init__(self, name):
        self.__name = name

    @classmethod
    def shout_count(cls):
        print('Animal shout')

    @classmethod
    def shout(cls):
        print(cls, cls.__name__, 'shout')

    def eat(self):
        print('{} eat'.format(self.__class__.__name__))


class Garfield(Animal):
    def __init__(self, name, weight, height):
        # super方法，很方便的访问祖先类，
        # 等价于self.__class__.__base__.__init__(self, name)
        # 等价于Animal.__init__(self, name)
        super(Garfield, self).__init__(name)
        # Animal.__init__(self, name)
        self.name = name

    def eat(self):
        print('{} eat'.format(self.__class__.__name__))

    @staticmethod
    def shout_count():  # override
        print('Garfield shout count')


if __name__ == '__main__':
    cat = Garfield(3, 5, 15)
    cat.shout_count()
    cat.shout()
    cat.eat()
    print(cat.__dict__)
    print(Garfield.__dict__)
    print(Animal.__dict__)
