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
如下，B类定义时声明继承自A类，在B类的`__bases__`中可以看到A类。但是这和是否调用A类的初始化方法`__init__`是两回事。
如果B中调用了A的初始化方法`__init__`，就可以拥有父类的属性。如下，在B的初始化方法`__init__`中，先调用了A类的初始化方法，
且与B的实例self绑定，则B拥有了A的实例属性，然后重新定义了self.b，覆盖继承的A类的属性的值，并新增了self.C.

*良好的编码习惯，如果父类定义了初始化方法`__init__`，则子类应该调用一下父类A的`__init__`

什么时候子类会自动调用父类的初始化方法`__init__`:
子类C未重新初始化方法，则子类C初始化会自动调用基类B的`__init__`方法。注意：其查找顺序遵从`__mro__`，第一次找到祖先类的`__init__`立即返回。
子类一旦重写了初始化方法`__init__`，就不会自动调用父类的`__init__`，必须显式调用才会好拥有父类的实例属性。
四、多继承
多继承很好的模拟了世界，因为事物很少是单一继承。但是多继承使问题复杂化；舍弃简单，必然引入了复杂性，带来了冲突。
比如：一个孩子继承了来自父母双方的特征。那么到底眼睛像爸爸还是妈妈呢？孩子究竟该像谁多一点呢？
多继承的现导致编译器设计的复杂度增加，所有很多语言舍弃了类的多继承。C++支持多继承，Java舍弃了多继承。
多继承可能会带来二义性，例如猫和狗都继承自动物类，现在如果一个类多继承了猫和狗类，猫和狗都有shout方法，子类究竟继承谁的shout呢？
解决方案：实现多继承的语言，要解决二义性，深度优先或广度优先。
五、Python多继承实现
class ClassName(基类列表)：
    类体
多继承带来路径选择问题，究竟继承哪个父类的特征呢？python使用MRO(method resolution order)解决基类搜索顺序问题。
历史原因，MRO有三个搜索算法。C3算法，类被创建出来的时候，就计算出一个MRO有序列表。没必要深入理解C3算法，类设计出来后，
子类需要查看搜索顺序，直接执行`SubClass.__mro__`就行了。
多继承的缺点：控制多继承的规模，不管编程语言是否支持多继承，都应当避免多继承。
项目开始时，一定要约定好，怎么命名变量名、类名、类的继承等等。
当类很多，继承复制的情况下，继承路径太多，很难说清什么样的继承路径。
python语法是允许多继承，但python代码是解释执行，只有执行到的时候才发现错误。
团队协作开发，如果引入多继承，那代码将不可控。
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
