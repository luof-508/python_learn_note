#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: object_oriented_05.py
五、访问控制
    - **私有属性，** 本质是类定义的时候，如果声明了一个实例变量的时候，使用双下划线，python解释器会将其改名，转换为`_类__变量名`的名称。
    而在实例化后，动态赋值的属性，比如`tom.__age=100`，非类定义的时候，解释器不会改名。
    - **保护变量：** 和普通属性一样，解释器不做任何特殊处理，只是开发者的共同约定，看见这种变量，就如同私有变量，不要直接使用。
    - 知道私有属性的新名称后，外部也可以绕过直接访问、修改。

    - 在python中，使用`_`单下划线或者`__`双下划线来标识一个成员被保护或者被私有化隐藏起来。但是不管使用什么
    样的访问控制，都不能真正阻止用户修改类的成员。Python中没有绝对安全的保护成员或者私有成员。
    - 因此，前导下划线只是一种警告或者提醒，需要遵守这个约定，不要**破坏封装**。

"""


class Person:
    def __init__(self, name):
        self._name = name  # 保护变量，内部函数或内部变量，不要引用
        self.__age = 18  # 私有属性

    def age_up(self, num: int):
        if 0 < self.__age < 150:
            self.__age += num

    def get_age(self):
        return self.__age

    def __growup(self, incr=1):
        if 0 < incr < 150:
            self.__age += incr


if __name__ == '__main__':

    tom = Person('tom')
    # print(tom.__dict__)
    # print(tom._Person__age)
    # tom._Person__age = 180
    # tom.__age = 100
    # print(tom.__dict__)
    # tom._name = 'jerry'
    # print(tom.__dict__)
    # 私有方法
    tom._Person__growup()
    print(tom.__dict__)
    print(tom.__class__.__dict__)


