## 10 封装（Encapsulation）
- 将数据和操作组织到类中
- 将数据隐藏起来，给使用者提供操作。使用者通过操作就可以获取或修改数据，getter，setter
- 通过访问控制，暴露适当的数据和操作给用户，该隐藏的隐藏起来，保护成员和私有成员
***

## 11 继承(Inheritance)
如前所述：人类Person和猫类Cat都继承自动物类Animal  
个体继承自父母，继承了父母的一部分特征，但也可以有自己的个性。  
在面向对象的世界中，从父类继承，就可以直接拥有父类的属性和方法，这样可以**减少代码、多复用**。
子类可以定义自己的属性和方法。  

**继承：** Class SubClassName(FatherClassName)，这种形式就是从父类继承，括号中写上继承的类的列表。  
**继承可以让子类从父类获取特征（属性和方法）**  

**父类：** 又称基类、base类、超类
**子类：** 又称派生类

**继承定义：** Class子类名(基类1[,基类2,...])；如果没有基类列表，等同于继承自object类。
python3中object类是所有对象的根基类

**继承的特殊属性和方法：**  
|属性|含义|说明|  
|:-:|:-:|:-|  
|`__base__`|类的基类|  
|`__bases__`|类的基类元组|实例无此属性  
|`__mro__`|显示方法查找顺序，返回基类的元组|返回元组|  
|`mro()`|同`__mro__`|`__mro__`就是mro()的返回值，但是mro()是一个列表|  
|`__subclasses__()`|所有子类列表|列表|  

**示例：**  
```python
class Animal:
    HEIGHT = 0
    __COUNT = 0

    def __init__(self, age, weight, height):
        self.__age = age
        self.__weight = weight
        self.HEIGHT = height

    @classmethod
    def shout_count1(cls):
        print(cls.__COUNT)

    def __get_weight(self):
        print(self.__weight)

    def eat(self):
        print('{} eat'.format(self.__class__.__name__))


class Garfield(Animal):
    NAME = 'Garfield'

    def get_age(self):
        print(self.__age)


class Dog(Animal):
    def __init__(self, name):
        self.__name = name


if __name__ == '__main__':
    cat = Garfield(3, 5, 15)
    dog = Dog('dog')
    print(cat.HEIGHT)
    print(Animal.__dict__)
    print(Garfield.__dict__)
    print(cat.__dict__)
    print(dog.__dict__)
    print(cat.__class__.__mro__)
    print(Animal.__subclasses__())
    print(cat.__class__.__dict__)
    # print(cat.__COUNT)
    # print(cat.__get_weight)
    cat.shout_count1()
    cat.get_age()

```


**执行结果：**  
>15  
{'HEIGHT': 0, '_Animal__COUNT': 0, '__init__': <function Animal.__init__ at 0x000001CE620F9160>, 
'_Animal__get_weight': <function Animal.__get_weight at 0x000001CE623399D0>, 'eat': <function Animal.eat at 0x000001CE623393A0>, ...}  
{'__module__': '__main__', 'NAME': 'Garfield', 'get_age': <function Garfield.get_age at 0x000001CE62339AF0>, '__doc__': None}  
{'_Animal__age': 3, '_Animal__weight': 5, 'HEIGHT': 15}  
{'_Dog__age': 'dog'}  
(<class '__main__.Garfield'>, <class '__main__.Animal'>, <class 'object'>)   
[<class '__main__.Garfield'>, <class '__main__.Dog'>]  
...  
AttributeError: 'Garfield' object has no attribute '__COUNT'  
AttributeError: 'Garfield' object has no attribute '__get_weight'  
> 

**结论：**  
- 从Garfield的实例cat的属性字典`__dict__`和Animal类的属性字典可以看出，继承符合私有属性的定义。
类中以`__`双下划线开头的属性，属于私有成员，python解释器会自动将其重命名为`_类名__属性名`。
实例属性`self.__age`是在Animal类中声明的，所以解释器将其重命名为`_Animal__age`；而Garfield类
继承自Animal类，**实例属性和类属性依然遵从私有属性的规则**:私有`self.__age`在Animal类中定义的，
所以是Animal类私有的，即使子孙类也不能拥有。
- 类的属性只保存一份到`__dict__`中；子类的`__dict__`不会保存继承自父类的属性，需要的时候从父类
找就可以了，例如`cat.__class__.__mro__； 子类的`__dict__`仅保存子类新增的属性。  
- 继承时，公有的，子类、实例都可以访问；而私有成员被隐藏，子类和实例不可以直接访问，例如：执行
`print(cat.__COUNT)`时报`AttributeError: 'Garfield' object has no attribute '__COUNT'`错误，
只有私有变量`__COUNT、self.__age、self.__weight`所在Animal类的方法才可以访问这个私有变量。
- Dog类重写了初始化方法`__init__`，因此Dog类未继承父类的实例属性，只有重写初始化方法中定义的一个实例属性`{'_Dog__name': 'dog'}`
- 属性的查找顺序：实例的`__dict__` ->类的`__dict__` -> 父类的`__dict__`，先找到立即返回，一直找到object类未找到抛异常。

### 11.1 方法重写override  
super方法，很方便的访问祖先类；**静态方法、类方法、一般属性都可以被重写覆盖。**  
**示例：** 
```python
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
```
**执行结果：** 
>Garfield shout count  
<class '__main__.Garfield'> Garfield shout  
Garfield eat  
{'_Animal__name': 3, 'name': 3}  
{'eat': <function Garfield.eat at 0x000002B2FFC49B80>, 'shout_count': <staticmethod object at 0x000002B2FFA31340>,...}  
{'shout_count': <classmethod object at 0x000002B2FFA041F0>, 'shout': <classmethod object at 0x000002B2FFA040A0>, 'eat': <function Animal.eat at 0x000002B2FFC493A0>, ...}  

**总结：** 
- 子类Garfield实例cat调用继承自父类shout属性的调用，从执行结果`<class '__main__.Garfield'> Garfield shout`
可以看出，虽然属性定义在父类， 但是cls由传入的参数决定，cls传入的是Garfield，所以打印的`__name__`是Garfield
- 被重写的属性，在子类的`__dict__`就会保存这个属性，而继承的属性，只会保存在父类的`__dict__`中。

### 11.2 继承中的初始化
如下示例1，B类定义时声明继承自A类，在B类的`__bases__`中可以看到A类。**但是这和是否调用A类的初始化
方法`__init__`是两回事**。  
- **示例1，B调用了A的初始化方法`__init__`，所以拥有父类A的实例属性**。  
>示例1中，B的初始化方法`__init__`先调用了父类A类的初始化方法，且与B的实例self绑定，所以B拥有了
> 父类A的定义的实例属性`self.a`和`self.b`；然后B又重新定义了`self.b`，覆盖继承自A类的实例属性
> `self.b`，并新增了示例属性`self.c`。  
- 如果B类的初始化方法`__init__`中没有显式调用父类A的初始化方法，解释器不会自动调用，B的实例不会拥有实例属性`self.a`。  

**示例1：**
```python
class A:
    def __init__(self, a, b):
        self.a = a
        self.b = b

     
class B(A):
    def __init__(self, a, b):
        A.__init__(self, a+b, a-b)
        self.b = a
        self.c = b
    
    def printf(self):
        print(self.b)
        print(self.c)

        
class C(B):
    pass

if __name__ == '__main__':
    f = B(2, 3)
    print(f.__dict__)
    print(f.__class__.__bases__)
```
**执行结果：**
>{'a': 5, 'b': 2, 'c': 3}  
(<class '__main__.A'>,)  

**小结：良好的编码习惯，如果父类定义了初始化方法`__init__`，则子类应该调用一下父类A的`__init__`**

**什么时候子类会自动调用父类的初始化方法`__init__`？**  

1. 子类C未重新初始化方法，则子类C初始化会自动调用基类B的`__init__`方法。  
**注意：其查找顺序遵从`__mro__`，第一次找到祖先类的`__init__`立即返回。**  
2. 子类一旦重写了初始化方法`__init__`，就不会自动调用父类的`__init__`，必须显式调用才会好拥有父类的实例属性。  

**示例2：**
```python
class Animal:
    def __init__(self, age):
        self.__age = age

    def show(self):
        print(self.__age)


class Garfield(Animal):
    def __init__(self, age, weight):
        # 调用父类的__init__方法的顺序，决定了show方法的执行结果
        # 如果实例属性是私有成员，会发现，又有不一样的结果
        super(Garfield, self).__init__(age)
        self.age = age + 1
        # super(Garfield, self).__init__(age)

    def get_age(self, default=8):
        # 父类的初始化方法可以在子类的任何地方调用，调用位置不同可能引起不同结果，这一点一定要注意。
        super(Garfield, self).__init__(default)


if __name__ == '__main__':
    cat = Garfield(9, 5)
    cat.show()
    print(cat.__dict__)

```
**小结：父类的初始化方法可以在子类的任何地方调用，调用位置不同可能引起不同结果，这一点一定要注意。**  

### 11.3、多继承  
多继承很好的模拟了世界，因为事物很少是单一继承。

**1. 多继承的弊端：**
- 多继承使问题复杂化；舍弃简单，必然引入了复杂性，带来了冲突。  
>比如：一个孩子继承了来自父母双方的特征。那么到底眼睛像爸爸还是妈妈呢？孩子究竟该像谁多一点呢？  

- 多继承的实现导致编译器设计的复杂度增加。所有很多语言舍弃了类的多继承，C++支持多继承，Java舍弃了多继承。  

- 多继承可能会带来二义性。
>例如猫和狗都继承自动物类，现在如果一个类多继承了猫和狗类，猫和狗都有shout方法，子类究竟继承谁的shout呢？  

**解决方案：实现多继承的语言，要解决二义性，深度优先或广度优先。**  

**2. Python多继承实现**  

```python
class ClassName('基类列表'):
    '类体'
```
多继承带来路径选择问题，究竟继承哪个父类的特征呢？  
**python使用MRO(method resolution order)解决基类搜索顺序问题。**  
>历史原因，从python的最初版本到python3，MRO一共有三个搜索算法。2.3之后唯一支持C3算法。
C3算法，在类被创建出来的时候，就计算出一个MRO有序列表。
没必要深入理解C3算法，类设计出来后，需要查看子类继承的搜索顺序，直接执行`SubClass.__mro__`就可以了。

**多继承的缺点：** 
- 当类很多，继承复制的情况下，继承路径太多，很难说清什么样的继承路径。
- python语法是允许多继承，但python代码是解释执行，只有执行到的时候才发现错误。
- 团队协作开发，如果引入多继承，那代码将不可控。  

**不管编程语言是否支持多继承，都应当避免多继承。**  
项目开始时，一定要约定好，怎么命名变量名、类名、类的继承等等。
