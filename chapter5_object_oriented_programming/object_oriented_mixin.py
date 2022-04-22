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

- 上述方案，是最传统、典型的类继承、设计流程。
- 用装饰器增强一个类，把功能给附加上去，哪个类需要就装饰它，动态添加、简单方便。


Mixin可以做类的继承，比装饰器更加灵活。Mixin，需要混进去的的功能非常多，这个时候用Mixin类来做比用装饰器更好。
简单问题，装饰器两下搞定，复杂问题，用Mixin更加清晰；二者都很高大上。

组合的设计模式：
Mixin,本质上是多继承实现的，体现了一种更加流行、重要的设计模式--组合的设计模式。**缺什么补什么**。
继承是一种设计模式，继承其实叫泛化，但是组合更好。通过多继承，把需要增强的类放到多继承的列表里面去，混合起来，实现很强的功能。
多种不同功能的类，混合在一起，实现更强大的功能。

比如要造机器人：缺胳膊，加胳膊；缺腿加腿；缺轱辘加轱辘。而不是通过继承，通过继承，上面的基类就需要更加丰富，基类不丰富，则机器人类就要非常丰富；那
如果以后要动态增加更多功能呢，现在的机器人只能走，但是保不齐以后机器人可以飞、可以潜水呢？
所以不要以固定思维设计未来这个类，因为类的功能都是动态变化的，不可能在设计之初就覆盖未来的所有功能。所以就用Mixin方式，组合。组合是优于继承的。

组合说到底也是继承，它是多继承，但是实现了一种组合的设计模式。能少继承，则少继承，其他方式用组合的方式来实现。
组合是需要的功能，写一个实现这个功能的类，把这个功能放在多继承列表的前面，组合过来；而不是在已经继承的基类上实现需要的所有功能，然后继承过来，因为
需求、功能随着发展动态变化，根本无法做到在基类上实现所有功能。缺什么补什么呗。

使用原则：
    1. Mixin类不应显示的出现`__init__`，为什么，你是混进去增强功能的，初始化干嘛呀，增强的东西相当于都是类属性，而不是增强实例的属性。
    2. Mixin类通常不能独立工作。为什么，就像机器人的例子，它只是一条腿、胳膊，是组合用的。
    3. Mixin类如果有继承发生，Mixin的祖先类应该也是Mixin类。
使用时，Mixin类通常在继承列表的第一个位置，例如class PrintableWord(PrintableMixin, Word):pass

Mixin和装饰器，这两种方式都非常好，都是一种组合的设计模式，看个人喜好。
推荐书籍：有足够的实践后，看看UML

"""


# 方案一、继承、重写
import json
import pickle


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


# 方案四、通过Mixin，缺什么补什么，比如Pdf类，要实现实现网络传输，缺序列化功能
class SeriaPdfMixin:
    def serialization_content(self, content):
        return pickle.loads(content)


class SeriaPdf(SeriaPdfMixin, Pdf):
    pass


if __name__ == '__main__':
    print(JsonableWord.__dict__)
    print(SeriaPdf.__mro__)
    print(SeriaPdf.__class__.__dict__)

