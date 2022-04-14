#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/13
@File: object_oriented_06.py
六、补丁
    补丁的意义：项目中一批类临近发布版本了，发现有几个类缺东西、缺功能了，，需要加东西，但又不想大规模修改源码。大规模修改源码要重新转测、重新发布很麻烦。怎么办，
        写一个文件，临时增加，下次发布版本的时候再打包进来。写一个文件，放到里面，文件的内容，就是找到对应要增加功能的类，为这些类增加属性、或替换属性。
    补丁：通过修改或替换类的成员（属性）。使用者调用的方式没有改变，但是类提供的功能可能已经改变了。

    打补丁属于事后发现，是一种临时措施。

猴子补丁：在运行时，对属性进行动态替换。就是把类添加、修改属性的过程，封装到某个函数、某个类、某个模块里。
    要么在对象的属性上替换，要么在类的属性上替换。

外部修改，破坏了封装，临时用用

七、属性装饰器：
作用：把实例的属性保护起来，不让外部直接访问，外部使用getter方法读取属性，setter方法设置属性

八、对象销毁
对象销毁。类中可以定义＿del＿方法。有对象的初始化，就有对象的销毁。
初始化，有可能包含其他对象，比如链接网络、连接数据库，这些对象创建后，当当前实例要消亡的时候，需要关闭创建的这些对象（收尾工作）。
在对象中定义＿del＿，在对象消亡前自动掉del＿方法，就可以完成上述收尾。python的垃圾回收不知道什么执行，类中定义＿del＿方法是有必要的

九、方法重载（overload）：其他面向对象的高级语言中才有重载的概念。
    所谓重载，就是同一个方法名，但是参数数量、类型不一样。就是同一个方法的重载。
    python没有重载，也不需要重载，python方法定义中，形参非常灵活，不需要指定类型，送进去是什么类型就是什么类型，参数个数也不固定。
    python在继承中有重写override，重写一个方法。
    重载是面向对象的一种方式，解决多态问题。
函数级多态：一个函数解决了多种参数类型，或返回多种类型

十、封装（Encapsulation）：
    1将数据和操作组织到类中
    2将数据隐藏起来，给使用者提供操作。使用者通过操作就可以获取或修改数据，getter，setter
    3通过访问控制，暴露适当的数据和操作给用户，该隐藏的隐藏起来，保护成员和私有成员

"""


class Person:
    """三种方式实现getter、setter方法

    为了保护对象属性，不破坏封装，通常在设计的时候，提供属性的访问方法(读取、修改)：getattr, setattr
    """
    def __init__(self, chinese, english, history):
        self.__chi = chinese
        self._eng = english
        self.__his = history

    def get_chi(self):
        print('get chi')
        return self.__chi

    def set_chi(self, val):
        print('set chi={}'.format(val))
        self.__chi = val

    def del_chi(self):
        print('delete chi')
        del self.__chi

    @property
    def eng(self):
        print('get eng')
        return self._eng

    @eng.setter
    def eng(self, val):
        print('set eng={}'.format(val))
        self._eng = val

    @eng.deleter
    def eng(self):
        print('delete eng')
        del self._eng

    def set_his(self, val):
        print('set his={}'.format(val))
        self.__his = val

    def del_his(self):
        print('delete his')
        del self.__his

    his = property(lambda self: self.__his, set_his, del_his, 'this is his property')


class MyClass:
    # 对象销毁。类中可以定义＿del＿方法。有对象的初始化，就有对象的销毁。
    # 初始化，有可能包含其他对象，比如链接网络、连接数据库，这些对象创建后，当当前实例要消亡的时候，需要关闭创建的这些对象（收尾工作）。
    # 在对象中定义＿del＿，在对象消亡前自动掉del＿方法，就可以完成上述收尾。python的垃圾回收不知道什么执行，必要的时候定义＿del＿方法＿是有必要的
    def __init__(self, name):
        self.name = name
        self.age = 18

    def __del__(self):
        print('delete {}'.format(self.name))


if __name__ == '__main__':
    stu = Person(97, 98, 99)
    # 方式一，函数方法设置属性访问控制
    print(stu.get_chi())
    stu.set_chi(70)
    print(stu.__dict__)
    stu.del_chi()
    print(stu.__dict__)
    print('*' * 20)
    # 方式二，@property装饰器方式访问控制
    print(stu.eng)
    stu.eng = 60
    print(stu.__dict__)
    del stu.eng
    print(stu.__dict__)
    print('*' * 20)
    # 方式三、property类实例方式访问控制，应用较多
    print(stu.his)
    stu.his = 9
    print(stu.__dict__)
    del stu.his
    print(stu.__dict__)

    tom = MyClass('tom')
    del tom
