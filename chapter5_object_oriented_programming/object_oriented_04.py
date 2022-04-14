#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: object_oriented_04.py
四、类方法和静态方法：

类方法：
    * 在类中，使用`@classmethod`装饰器修饰的方法。类方法至少有一个参数，且第一个参数必须是cls，cls指
    类对象自身。cls和self一样，也只是一个标识符，可以是任意合法名称，默认都用cls。
    * 作用：**通过cls，直接操作类的属性，增加、修改类属性。**
    * Python的类方法，类似于C++、Java中的静态方法
静态方法：
    * 在类定义中，使用@staticmethod装饰器修饰的方法。
    * 调用静态方法时，Python解释器不会隐式的传入参数，静态方法相当于普通函数，只是被类这个名称空间组织管理。
总结：
    类不能调用普通方法，因为普通方法第一个参数必须是类的实例。
    实例可以调用类中定义的所有方法；普通方法传入实例本身作为第一个参数， 静态方法和类方法本质是先调用__class__找到类，再调用方法；
    `normal_mtd()`虽无语法错误，但不允许在类中这样定义。
"""


class Person:
    # 1.`a.foo()`调用过程：实例a调用与a绑定的类属性foo，Python解释器将实例a作为位置参数self的实参传入。
    # 2.`MyClass.bar()`调用过程：MyClass可以理解为一个包含各种属性的名词空间，`bar`只是被MyClass这个名词空间管理的一个普通方法，从自己的
    # 属性`__dict__`中通过`key = 'bar'`调用普通方法bar。
    # 3.`a.bar()`调用过程：类的实例a通过`__class__.__dict__`找到类的属性bar，同时Python解释器将实例a作为实参传入，但是由于类属性bar第一个
    # 参数不是self，无法完成与实例a的绑定，导致无法调用，报`TypeError: bar()takes 0 positional arguments but 1 was given`。
    def normal_mtd():
        # 虽然无语法问题，但是不要这样写，使用静态方法代替
        print('normal')

    def mtd(self):
        print("{}'s method".format(self))

    @classmethod
    def class_mtd(cls):
        print('class = {0.__name__} ({0})'.format(cls))
        cls.HEIGHT = 170

    @staticmethod
    def static_mtd():
        print(Person.HEIGHT)


if __name__ == '__main__':
    # 类调用
    print('类调用')
    print(1, Person.normal_mtd())  # 虽然无语法问题，但是不要这样写，使用静态方法代替
    # print(2, Person.mtd())  # 调用普通方法
    print(3, Person.class_mtd())  # 调用类方法
    print(4, Person.static_mtd())  # 调用静态方法
    # 实例调用
    print('实例调用')
    tom = Person()
    # print(5, tom.normal_mtd())
    print(6, tom.mtd())  # 调用普通方法
    print(7, tom.class_mtd(), tom.__class__.class_mtd())  # 调用类方法  tom.mtd()等价于tom.__class__.class_mtd()
    print(8, tom.static_mtd(), tom.__class__.static_mtd())  # 调用静态方法  tom.mtd()等价于tom.__class__.static_mtd()
