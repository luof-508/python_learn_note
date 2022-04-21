#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/21
@File: object_oriented_mixin.py
十二、Mixin
1、文档类Document是所有文档类的抽象基类。Word、Pdf是Document的子类。
需求：为Document的子类提供打印能力
分析：因为Document的子类都具有打印能力，因此printf方法定义在Document中比较合适，这样属性只在Document的`__dict__`保留一份就可以了。
基类提供的printf方法不应具体实现，因为它未必适合子类的打印；子类Word、Pdf需要个性化，继承、重写就好了。

上述方案在以下场景又不太合适，比如：
Word、Pdf类都继承自Document类，且都是属于第三方库，不允许重写；又或者一个大型项目中有其他继承自Word类的子类，这些子类继承了Word类的printf方法。
这个时候通过继承、重写实现需求，则违反了开闭原则。
如何解决？
继承后重写：PrintableWord(Word)

对于一个类有非常多的子类，且这些子类要继承、重写实现不同的功能，上述方案会导致太多的子类，非常繁琐。
比如，Word子类应用网络中，应具备序列化功能，那子类中就应该实现序列化；但是序列化又有pickle、json、messagepack等，难道每种功能继承、重写
一个子类吗？那又要实现序列化又要具备打印、甚至更多功能呢？所有会产生太多的子类，过于繁琐。
如何解决？
装饰器类：


"""


# 方案一、继承、重写
class Document:
    def __init__(self, content):
        self.content = content

    def printf(self):
        print(self.content)


class Word(Document):  # 第三方库，不允许重新
    def printf(self):
        print('This content:{}'.format(self.content))


class Pdf(Document):  # 第三方库，不允许重新
    pass


# 方案二、继承后重写，避免违反开闭OCP原则
class PrintableWord(Word):
    def printf(self):
        print('This is printable:{}'.format(self.content))


# 方案三、通过装饰类，删减、增加功能
def jsonable(cls):
    import json
    cls.jsonable = lambda self: json.dumps(self.content)
    return cls


@jsonable
class JsonableWord(Word):
    pass


if __name__ == '__main__':
    print(JsonableWord.__dict__)
