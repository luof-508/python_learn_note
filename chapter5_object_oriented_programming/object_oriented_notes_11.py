#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/28
@File: object_oriented_notes_11.py

四、运算符重载：
    比较运算符：自定义类的时候，需要用到，内建类型都重写过了。比如坐标类，如何比较大小，自己不给出的话，就调用Object了。
    运算符重载最好的例如：pathlib.Path()/'a'/'b'
    需要什么补充什么。写在类内部更好。需要的时候补充就行，可以看int的源码，几乎实现了所有操作符重载的魔术方法，也可以看帮助文档
    应用场景：主要运用于面向对象实现的类，需要做大量运算的场景，运算符是这种运算在数学上最常见的表达式。比如实现Point类相加的二元操作：`Point + Point`,
    通过定义`__add__`方法，重载加法运算符+。提供运算符重载，比直接提供加法add更加适合该领域内使用者的习惯。所以好的类的设计，有运算需求，就应该提供运算符重载。

五、容器相关方法：
    1、`__len__`：长度。内建函数len(obj)，调用的就是`obj.__len__()`。如果没有提供将抛错，其实就是把对象当做容器类型看，就如同list或dict。bool()函数
    调用的时候，如果没有`__bool__`，就会看有没有`__len__`。注意有些第三方库len和size不是一个动作，size指的是内存中有多少个格子存放东西，而len才指元素的个数。
    2、`__liter__`：迭代。迭代容器时调用，返回一个新的迭代器对象。因此给出`__liter__`时，必须return一个迭代器。
    迭代很重要，很多时候，关心的容器能不能迭代，有没有我想要的东西在里面。
    3、`__contains__`：in成员运算符。不同容器有不同实现方法，比如列表，就一个一个找，字典求hash速度很快；所以可以不提供，不提供就调用＿iter＿方法遍历。
    4、`__getitem__`：实现`self[key]`访问。注意不仅限于dict，不要被key迷惑，列表，元组都可以，这个时候key就是索引。所以：对于序列对象（例如购物车类Cart），
    key接受整数为索引，或者切片（可见，切片调用的就是`__getitem__`）；对于set或dict，key为hashable。key不存在引发keyError异常。

    5、	`__setitem__`：与`__getitem__`类似，就是根据中括号给的索引或者给的key，然后找到置，把值塞进去。对于序列对象key超界，引发IndexError。
    6、`__missing__`：对于dict／set类型对象，调用`__getitem__`，但塞进去的是一个不存在的key，通过`__missing__`处理修正

六、可调用对象：python中一切皆对象，函数也不例外
    `__call__`：对象obj加上（），就是调用对象的`__call__()`方法。obj()等价于`obj.__call__()`。
    意义：类中定义一个＿cal

"""
import operator


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):  # 运算符重载实现向量运算
        return Point(self.x + other.x, self.y + other.y)

    def add(self, other):  # 直接实现向量加法运算
        return Point(self.x + other.x, self.y + other.y)


class A:
    def __init__(self, x):
        self.x = x

    def __sub__(self, other):
        return self.x - other.x

    def __ne__(self, other):
        return self.x != other.x

    def __eq__(self, other):
        return self.x == other.x

    def __lt__(self, other):
        return self.x < other.x

    def __iadd__(self, other):
        # return A(self.x + other.x)  new一个新对象
        self.x += other.x
        return self  # 就地修改


class Item:
    def __init__(self, name, price, *attr):
        self.name = name
        self.price = price
        self.attr = attr

    def __repr__(self):
        return self.name + ' price:' + str(self.price)


class Cart:
    def __init__(self):
        self.__items = []

    def __repr__(self):
        return str(self.__items)

    def __add__(self, other):
        self.__items.append(other)
        return self  # 这里为什么返回self，体现的是链式编程思想

    def __iter__(self):  # 实现迭代，注意：要求返回必须是一个迭代器。实现迭代方法，相比直接取self.items进行迭代，没有把属性暴露出去，更好
        return iter(self.__items)

    def __len__(self):
        return len(self.__items)

    def __getitem__(self, idx):
        return self.__items[idx]

    def __setitem__(self, key, value):
        self[key] = value


class Fib:
    def __init__(self):
        self.ret = [1, 1]  # 给出前2项常数值

    def __call__(self, idx):
        return self[idx]

    def __getitem__(self, key):  # 给出__getitem__，实现obj[key]操作
        if key < self.__len__():
            return self.ret[key]
        for idx in range(self.__len__(), key):
            self.ret.append(self.ret[idx-1] + self.ret[idx-2])
        return self.ret[-1]

    def __len__(self):
        return len(self.ret)

    def __iter__(self):
        return iter(self.ret)

    def __str__(self):
        return str(self.ret)

    __repr__ = __str__


if __name__ == '__main__':
    # p1 = Point(1, 2)
    # p2 = Point(3, 4)
    # print(p1 == p2)
    # print(p1 + p2)  # 相比通过加法函数相加print(p1.add(p2))，运算符重载更符合相关专业人士的使用习惯
    ###############
    # car = Cart()
    # print(car + Item('item1', 12) + Item('item2', 1) + Item('item3', 8))  # 链式编程加法，等价于:
    # # car.__add__(Item('item1', 12)).__add__(Item('item2', 1)).__add__(Item('item3', 8))
    # print(len(car))  # 长度
    # for x in car: print(x)  # 迭代，相比取self.items进行迭代，没有把属性暴露出去，更好
    # print(car[2])  # 索引操作，调用__getitem__
    # car[2] = Item('item_x', 58)  # 调用__setitem__
    f = Fib()
    print(f(1))
    print(f(2))
    print(f(5))
    print(f(8))
    print(f[8])


