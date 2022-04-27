#!/usr/bin/env python3
# coding=utf-8
"""
十三、python的魔术方法
    魔术方法是其他语言没有的方法
|名称|含义|说明|
|:-:|:-:|:-|
|__name__|类、函数、方法等的名字|实例没有＿module＿：模块，序列化的时候会记住module，一个module可以认为是一个名词空间
|__bases__|类的基类的元组|__bases__不是mro，只是基类列表中的按顺序出现的一个列表
|__mro__|类的mro，多继承的属性查找顺序|class.mro()返回的结果保存在__mro__中
|__dict__|类或实例的属性，可读写的字典
|__class__|对象或类的所属类


**查看属性dir()**:
|方法|意义|
|:-:|:-|
|`__dir__`|返回类或对象的所有成员名称列表。dir()函数就是调用__dir__()。如果提供__dir__()，则返回属性的列表，否则会尽量从__dict__属性中收集信息,
dir详细说明可追源码。

import导入的是名词空间，比如import time,
##	魔术方法：
    分类：
        - 创建与销毁：`__init`,`__new`，`__del__`
        - hash：
        - bool：
        - 可视化：
        - 运算符重载：
        - 容器和大小：
        - 可调用对象：
        - 上下文管理：
        - 反射：
        - 描述器：
        - 其他杂项：

一、__hash__:
|`__hash__`|内建函数hash()调用的返回值，返回一个整数。如果对象中定义了这个方法，这个对象的实例就是可hash的。
hash和去重是两回事。去重set 先做is，然后再做==
    - hash默认是对内存中的地址求hash值。hash原理都是一样，用取模法去理解hash算法,那些一系列的复杂算法，不果就是让冲突域更大，冲突的可能性更小。
    - hash一定会有冲突，不可避免。hash值相同不代表两个对象是同一个东西，因此去重和hash是两回事。hash值相同，去重还要看值等不等。
|`__eq__`|对应==操作符，判断2个对象是否相等，返回bool值


二、`__bool__`：内建函数bool(obj)或者obj放在逻辑表达式位置时，首先调用的就是对象的`__bool__`方法，返回对象的bool值。
执行逻辑：obj没有定义`__bool__`，就找obj的`__len__`。如果`__len__`也没有定义，那么所有实例都返回为真。
list、set、dict等内置数据结构为空时，等效为False，原因就是定义了`__len__`魔术方法。
所以容器类型的往往不会实现__bool__方法，而会实现__len__方法

三、可视化:`__str__`，`__repr__`
|名称|含义|说明|
|:-:|:-:|:-|
|`__repr__`|执行内建函数repr(obj)时，就是调用`obj.__repr__()`,如果没有定义`__repr__`，则返回对象在内存中的地址。|
|`__str__` |执行内建函数str(obj)、format(obj)、print(obj)，首先调用`obj.__str__()`；如果没有定义`__str__`,则调用`obj.__repr__()`；如果`__repr__`也没有定义，则返回对象在内存中的地址。|
|`__bytes__`|执行内建函数bytes(obj)时，就是调用`obj.__bytes__()`，如果没有定义，抛错|

应用场景，当在使用str(obj)这种函数直接对一个对象obj取字符串表达的时候，就是调用对象的的可视化魔术方法，format、print方都是调用可视化模式方法。
调用逻辑： 内建函数str(obj)、format(obj)、print(obj)，首先调用对象`obj.__str__()`；如果没有定义`__str__`,则调用`obj.__repr__()`；
如果`__repr__`也没有定义，则返回对象在内存中的地址。

四、运算符重载:
"""
import time


class Animal:
    X = 123

    def __init__(self, name):
        self._name = name
        self.__age = 10


class Dog(Animal):
    pass


class Cat(Animal):
    def __dir__(self):
        return ['cat']


#  理解hash
class A:
    X = 123

    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __hash__(self):  # 不同实例hash冲突示例
        # __hash__必须返回一个整型
        # 一个对象定义了__hash__方法，就代表这个对象的实例可hash，但可hash，且hash值相等，不代表可去重
        # 追list的原码，可知，设计不可hash对象，定义对象属性__hash__ = None即可。
        # `__hash__`方法只是返回一个hash值作为set或者dict的key，可hash对象必须提供`__hash__`方法
        return 12

    def __eq__(self, other):  # 为什么需要相等函数
        # 注释掉Class A中的`__eq__`执行去重实例a,b，和不注释`__eq__`，再执行去重。从两次执行结果可以看出，set去重，默认先执行is,判断两个实例
        # 在内存中是不是同一个东西,后找==；如果要自定义去重方法，需要在对象中提供`__eq__`方法，这个时候去重则直接根据`__eq__`的结果进行处理。
        return self.y == other.y


def hash_(x):
    return x % 3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))  # 这里对象使用元组，是因为元组可hash

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return 'abc'

    def __str__(self):
        return '123'

    def __bytes__(self):
        return b'def'


if __name__ == '__main__':
    # ha = Dog('ha')
    # cat = Cat('Gard')
    # print(dir(Animal))
    # print(dir(Dog))
    # print(dir(ha))
    # print(ha.__dir__())
    # print(dir(Cat))
    # print(dir(cat))
    # print(dir())
    # print(set(list(ha.__dict__.keys())) | set(list(ha.__class__.__dict__.keys())) | set(list(object.__dict__.keys())))
    # # **从示例执行结果可以看出：**
    # 1. 对象Dog未定义属性`__dir__`时，`dir(Dog)`或`dir(ha)`，相当于先查找对象自己的`__dict__`->再查找对象的类的`__dict__`->再查找基类的`__dict__`;
    # 所以，除几个特色属性外，几乎等价于最后一行方法
    # 2. 对象Cat定义了`__dir__`时，执行`dir(cat)`,直接调用实例的`__dir__`方法。注意：**自定义`__dir__`时最好返回list**
    # 3. **import modulename，导入的是名词空间**
    # print(hash(A(5, 7)))
    # a = A(5, 7)
    # b = A(5, 7)
    # print(a, b)
    # print(a is b)
    # s = {a, b}
    # print(s)
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1 == p2)
    print(p1)
    print(p2)
    lst =[p1, p2]
    print(lst)
    print(*lst)
    print(list(map(str, lst)))
    print(bytes(p1))
