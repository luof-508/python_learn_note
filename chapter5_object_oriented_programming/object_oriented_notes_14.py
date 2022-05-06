#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/5
@File: object_oriented_notes_14.py
九、反射：
概念：**运行时**，指程序被加载到内存中执行的时候。区别于编译时。
反射，reflection，指运行时获取类型定义信息。一个对象能够在运行时，像照镜子一样，反射出其类型信息就是反射。简单的说，在python中，能够通过一个对象，找出其type、class、attribute或method的能力，称为 反射。例如：

Point类的实例p，通过反射能力，在`p.__dict__`中找到自己的attribute，并且修改、增加自己的attribute
通过`__dict__`获取、修改属性不优雅，python提供了内建函数：
|`getattr(object, name[, default])`|通过name返回 object的属性值。属性不存在返回default，如果没有给出default，抛AttributeError。|注意，name必须为字符串类型；<br>getattr搜索顺序，遵从mro搜索顺序，先从自己的`__dict__`中找，然后找class的...|
|`setattr(object, name, value)`|object的属性存在则覆盖，不存在新增。|注意：object为类则新增类属性，为实例则新增实例性。<br>--动态增加属性，未绑定。增加到实例，则在实例的__dict__中。|
|hasattr(object, name)|判断对象是否有这个名字的属性|name必须为字符串类型

**总结**：动态增加属性的方式，和装饰器修饰一个类、Mixin方式的差异在于，Mixin和装饰器在编译时就决定了；而动态增、删属性的方式是运用反射能力，运行时改变类或实例的属性，更灵活。
**示例：** 通过`getattr/setattr/hasattr`改造命令分发器

反射相关的魔术方法：`__getattr__、__setattr__、__hasattr__`:

"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Dispatcher:
    def reg(self, cmd: str, fn):
        if not hasattr(self, cmd):
            setattr(self.__class__, cmd, fn)
        else:
            raise Exception('Exist')

    def run(self):
        while True:
            cmd = input('enter:')
            if cmd == 'q':
                return
            getattr(self, cmd, self.default_func)()

    @classmethod
    def default_func(cls):
        print('default')


if __name__ == '__main__':
    # p = Point(2, 3)
    # # 运用对象的反射能力，在`p.__dict__`中找到自己的attribute，并且修改、增加自己的attribute
    # print(p.__dict__)
    # p.__dict__['x'] = 3
    # p.z = 12
    # print(p.__dict__)
    # #
    # setattr(Point, 't', 14)
    # print(p.__dict__)
    # print(getattr(p, 't'))
    # if not hasattr(p, 'lab'):
    #     setattr(p, 'lab', lambda x: print(x))
    #     setattr(Point, 'lab1', lambda self: print('lab1'))
    # print(p.__dict__)
    # print(Point.__dict__)
    # p.lab('lab')
    # p.lab1()
    dis = Dispatcher()
    dis.reg('cmd1', lambda self: print('cmd1'))
    dis.reg('cmd2', lambda self: print('cmd2'))
    dis.run()
