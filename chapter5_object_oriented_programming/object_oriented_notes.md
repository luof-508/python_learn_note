# 面向对象OOP：Object Oriented Programming

## 1 语言分类
**面向机器：** 汇编语言。抽象成机器指令，机器容易理解。  

**面向过程：** C语言。做一件事，排出先后顺序的步骤：第一步做什么、第二步做什么。问题闺蜜小，可以步骤化。  

**面向对象OOP：** C++、Java、Python。随着计算机需要解决的问题规模扩大，情况越来越复杂。需要很多人、
很多部分协作，面向过程无法解决这种大规模问题。

通过面向对象的思想，实现模块化开发，可以写很复杂的项目；有了很复杂的项目，进而诞生了软件工程。  
软件工程：对项目的管理；基于软件的管理学思想 --> 软件业诞生。
面向切面AOP也是面向对象的范畴


## 2 面向对象
***一种认识世界、分析世界的方法论。将万事万物抽象为类。*** OOP是最接近人类认知的编程范式。

**类class：** 类是抽象的概念，是万事万物的抽象，是一类事物的共同特征的集合。用计算机语言描述，就是
属性和方法。 类中定义的所有函数，都是类的方法；类中定义的变量，就是类的属性。例如人类：人类具有许多
共同的特征，用计算机语言描述就是人类的属性；人类可以走路、唱歌、吃饭等，这是人类的动作，用计算机语言
描述就是方法。  

**对象instance、object：** 对象是类的实例，是一个个实体。例如，李老师，是人类的一个具体对象；他
具有身高、体重、名字，这是李老师这个人类对象的属性，这些具体的个人属性不能保存在人类中，因为这是抽象
的概念，不能在人类中保留具体的值。  
***
**如何理解`一切皆对象`编程思想：**  
>例如：你吃鱼  
你，就是对象；鱼也是对象。  
你，是人类的一个具体对象，而人类是把全世界所有人具有的共同特征抽象后的概念，是无数具体的个体的抽象。    
鱼，也是具体的对象，属于鱼类，而鱼类是无数的鱼抽象出来的概念。  
吃，是动作，也是一种操作或方法，也就是人类具有的方法。  
吃，是很多动物都具有的动作，人类和鱼类都具有这个动作，因此，人类和鱼类都属于动物类。动物类又是一个抽象
的概念，是所有具有吃这个方法或动作的动物的集合，不同动物吃法不同，因此可以理解，动物类是人类和鱼类的
父类。  
你驾驶汽车，驾驶汽车这个动作是鱼类没有而人类有的，因此同一个动物父类下的各个子类又有各自的属性和方法。  


**属性**：它是对象状态的抽象，用数据结构来描述。  
**操作**：它是对象行为的抽象，用操作名和实现该操作的方法来描述。  
人类的名字、身高、体重等属性，是无数个人的属性抽象后的概念，因此人类不能保留这些属性的具体值。而人类的
实例，具体的人，例如李老师，他可以存储这些具体的属性；而且不同的人，这些属性的值各不相同。  

可见，一切皆对象，**对象是数据和操作的封装**，对象是独立的，但是对象之间可以相互作用(通过操作、方法)。
而在面向对象编程中，实现吃这个动作，又是一种面向过程的编程思想。

***类是属性和方法的集合，一个类又具有父类和各种各样的子类。在具体的项目中，需要根据项目规模、目的，进行
设计划分，抽象出需要的类，并抽象出不同类的属性和方法。***

***

## 3 *面向对象3要素  
**封装：**  
- 组装：将数据和操作组装到一起。
- 隐藏数据：对外只暴露一些接口，通过接口访问对象。比如驾驶员使用汽车，不需要了解汽车内部结构细节，只
需要怎么使用汽车，如何驾驶就行了。
**继承：**  
- 通过继承父类，复用父类的方法和属性，就不用每次都重写需要的属性和方法，只需写新增的方法或需要修改的
方法。
- 多继承少修改，OCP(Open-Closed Principle)开闭原则。使用继承来改变，体现个性。比如杀马特类继承
自人类，具有理发的方法，人类理发的方法都比较符合大众审美，但是杀马特类决定这个方法不好，自己要个性化，
这个时候就不能去修改人类的理发方法，而是在杀马特类重新定制自己的理发方法，避免影响其他继承自人类的类
的理发方法。
- 继承分为单一继承、多继承。

**多态：**  
- 面向对象编程最灵活的地方，动态绑定。子类实例化，赋给父类。
- python本身就是一个动态变化的东西，变量类型送进去的是什么类型才是什么类型。因此多态在python里不适
用，本身就是动态变化的。
- 多态，继承自动物类的人类、猫类的操作“吃”不同。

***不管千变万化，简单就是美***
***
## 4 python的类

### 4.1 类定义
```python
class MyClass:
    """A example class"""
    x = 123  # 类属性

    def foo(self):  # 类属性foo，也是方法
        # foo是类的方法，但是foo是一个标识符，只是标识符foo正好对应了这个函数实体，
        # 定义一个函数之后，这个函数标识符会对应到创建出来的函数对象上，类方法foo本质也是这样一个过程。
        return 'My Class'
```
类定义完成后，就产生了一个**类对象**，并绑定到了标识符ClassName上；类似函数定义完成后，这个函数
就是函数对象。  
**类对象**是指ClassName这个类，而**类的对象**是指类的实例，例如类的对象a:`a=ClassName()`。
所以，在python中一切皆对象。  

### 4.2 类对象及类属性  
**类对象**：类定义完成后，就会生成一个类对象，并将这个对象绑定到标识符ClassName。  
**类的属性**：类中定义的变量和类中定义的方法，都是类的属性。MyClass中，x、foo都是类的属性，
__doc__也是类的属性。  
**类变量**：x是类MyClass的变量  

**注意：**
1. foo方法是类的属性，如同**吃**是人类的方法，但是**每一个具体的人才能吃东西**，也就是说吃是人的
实例才能调用的方法。
2. foo是方法对象method，不是普通的函数对象function，它至少有一个参数self，且第一个参数必须是
self(self只是参数标识，可以换一个名字)，这个参数位置就留给了self。
3. **self指代当前实例本身**

### 4.3 实例化  
```python
class Person:
    """an example class"""
    x = 'abc'  # 类属性

    def __init__(self, name, age=18):
        # __init__()方法不能return一个返回值，也就是只能是None
        self.name = name
        self.y = age

    def __new__(cls, *args, **kwargs):
        pass

    def foo(self):  # 类属性foo，也是方法
        # foo是类的方法，但是foo是一个标识符，只是标识符foo正好对应了这个函数实体，
        # 定义一个函数之后，这个函数标识符会对应到创建出来的函数对象上，类方法foo本质也是这样一个过程。
        return 'my Class'

    def show(self, x, y):
        print(self.name, self.x, x, y)
        self.y = x  # 修改实例属性
        Person.x = x  # 修改类属性


if __name__ == '__main__':
    a = Person('tom')
    b = Person('tom')
    print('id a = {}, id b = {}'.format(id(a), id(b)))
    print(a is b)
    print(a.foo)
```
**1. python类的实例化过程：**  
* 构建一个人类的实例`Tom = Person('Tom')`。构建过程为：
python内部首先调用类方法`__new__`，实例化一个人类对象Tom，然后再调用实例方法`__init__`，
初始化实例对象Tom。`__new__`和`__init__`不管有没有在类中定义，实例化过程都会隐式调用。实例化后
获得的实例，是不同的实例，即使是使用了同样的参数实例化，也是得到不同的对象，例如人类实例对象a和b，
虽然他们名字都叫tom，但是两个完全不同的个体。 
* 实例化中，类方法会绑定到实例化对象中，示例执行结果：
>id a = 1289315976288, id b = 1289349799216  
False
<bound method Person.foo of <__main__.Person object at 0x000001CE67C09DF0>>

**2. __init__方法：**  
* `Tom = Person('Tom')`实例化过程中，实际上调用的是`__init__(self)`方法，其作用是对实例
进行**初始化**。初始化函数`__init__`可以有多个参数，但第一个位置必须是self。这里的self，就是
实例化后的Tom，看似实例化时只执行了`Tom = Person('Tom')`，并没有传入Tom，实际上python隐式
调用初始化函数`__init__`时，已经传入了Tom。所以，Person类属性中的self，就是每一个具体的实例
对象本身，而在**初始化函数`__init__`中，定义的`self.name`和`self.y`变量就是实例属性**。  

**3. 类属性和实例属性的访问：**  
- 实例Tom中的类方法`show`，访问的`self.name`，与外部访问的`Tom.name`是同一个东西；所以
  可以通过`self.y=23`或`Tom.y=23`访问或修改实例属性。
- **注意：** 虽然可以通过实例访问类属性`x=self.x`或`x=Tome.x`,但是**不能通过实例修改类属性**，
  `self.x=123`或`Tome.x=123`并不是修改了人类Person的属性x，而是为实例Tom增加了x属性。如下
  代码执行结果：
```python
class Person(object):
    """an example class"""
    x = 'abc'  # 类属性
    age = 2

    def __init__(self, name, age=18):
        # __init__()方法不能有返回值，也就是只能是None
        print('This is init')
        self.name = name
        self.y = age

    def __new__(cls, *args, **kwargs):
        # 创建对象的时候，python解释器首先会调用__new__方法为对象在内存中分配空间，并返回对象引用
        # python解释器获得对象的引用后，将引用作为第一个参数，传递给__init__方法
        # 重写__new__方法一定要return super().__new__(cls)
        # 否则python解释器得不到分配了空间的对象引用，就不会调用对象的初始化方法
        # 注意：__new__是一个静态方法，在调用时需要主动传递cls参数
        print('This is new')
        return super().__new__(cls)

    def foo(self):  # 类属性foo，也是方法
        # foo是类的方法，但是foo是一个标识符，只是标识符foo正好对应了这个函数实体，
        # 定义一个函数之后，这个函数标识符会对应到创建出来的函数对象上，类方法foo本质也是这样一个过程。
        return 'my Class'

    def show(self, x, y):
        print(self.name, self.x, x, y)
        self.y = x  # 修改实例属性
        Person.x = x  # 修改类属性

if __name__ == '__main__':
    tom = Person('Tom')  # 实例化、初始化
    jerry = Person('Jerry')
    print(tom.name, tom.age)
    print(jerry.name, jerry.age)
    print(Person.age)
    Person.age = 30
    print(Person.age, tom.age, jerry.age)
    print('===' * 3)
    print(tom.__dict__)
    tom.age = 18
    print(Person.age, tom.age, jerry.age)
    print(tom.__dict__)
```
**执行结果：** 
>This is new  
This is init  
This is new  
This is init  
Tom 2  
Jerry 2  
2  
30 30 30  
=========  
{'name': 'Tom', 'y': 18}  
30 18 30  
{'name': 'Tom', 'y': 18, 'age': 18}  


**4. 实例对象instance：**  
* 类实例化后得到的对象，就是**实例对象**，比如`Tom`和`Jerry`。`__init__`方法的第一个参数self
就是指代的某一个实例。
* 类实例化一个实例对象，实例对象会绑定类方法。例如人类实例Tom调用类方法show：
`Tom.show(x=2, y=3)`, 调用过程中为什么只传了两个参数？这个self就如上所述，就是Tom，Python
会把方法的调用者(这里就是Tom)作为第一个参数self的实参传进去。
* 对于实例Tom，`self.name`就是Tom的name，只有初始化后(调用了初始化函数__init__)，`self.name`才有
值。可见name是保存在人类Person的一个个实例中，而不是人类Person上。所以称为**实例变量**。
```python
class MyClass:
    def __init__(self):
        print('self in init = {}'.format(id(self)))


c = MyClass()  # 实例化，会调用__init__
print('c = {}'.format(id(c)))
```
打印结果为：  
>self in init = 1728871235648  
c = 1728871235648  

从打印结果可见：self就是调用者，就是c对应的实例对象；从打印顺序可见，实例化时调用了__init__。

**5. 实例变量和类变量**  
- **实例变量**是每一个实例自己的变量，是自己独有的；**类变量**是类的变量，是类的所有实例共享的
属性和方法。

**5.1 对象的特殊属性：**   
|特殊属性|含义|说明  
|:-:|:-:|:-|  
|`__name__`| 对象名 |不一定每个对象都有这个属性。<br>`tom.__name__`报错<br>`AttributeError: 'Person' object has no attribute '__name__'`,<br>因为tom只是Person类的一个实例的引用，所以没有`__name__`  
|`__class__`| 对象的类型|返回实例的对应的类  
|`__dict__`| 对象的属性的字典|对象的所有属性，保存存在字典中  
|`__qualname__`|类的限定名|指类定义时，被绑定的ClassName。<br>只有类才有这个属性，类的实例没有。  
```python
class Person(object):
    """an example class"""
    x = 'abc'  # 类属性
    age = 2
    height = 160

    def __init__(self, name, age=18):
        self.name = name
        self.y = age

    def foo(self):  # 类属性foo，也是方法
        # foo是类的方法，但是foo是一个标识符，只是标识符foo正好对应了这个函数实体，
        # 定义一个函数之后，这个函数标识符会对应到创建出来的函数对象上，类方法foo本质也是这样一个过程。
        return 'my Class'

    def show(self, x, y):
        print(self.name, self.x, x, y)
        self.y = x  # 修改实例属性
        Person.x = x  # 修改类属性


if __name__ == '__main__':
    tom = Person('Tom')  # 实例化、初始化
    jerry = Person('Jerry')
    # print(tom.__name__)  # tom只是Person类的一个实例的引用，所有没有__name__
    print(tom.__class__, tom.__dict__, tom.__class__.__qualname__)
    print(isinstance(jerry, tom.__class__))
    print(tom.__class__, tom.__class__.__name__)
    print(tom.__dict__)
    print(Person.__dict__, Person.__class__)

```
**执行结果：**  
>This is new  
This is init  
This is new  
This is init  
<class '__main__.Person'> {'name': 'Tom', 'y': 18} Person  
True  
<class '__main__.Person'> Person  
{'name': 'Tom', 'y': 18}  
{'__module__': '__main__', '__doc__': 'an example class', 'x': 'abc', <br>'age': 2, 'height': 160, '__init__': <function Person.__init__ at 0x00000216C2807160>, ...}

**从执行结果可见：** 类属性保存在类的`__dict__`中，实例属性保存在实例的`__dict__`中。如果从实例
访问类的属性，就要借助__class__找到所属的类。例如：实例tom访问类的属性x，
`tom.__class__.__dict__['x']`。

**结论：** 所有实例的操作方法都一样。所以对象(实例)的字典`__dict__`中没有必要保存方法，方法保存
到类的`__dict__`就可以了。

**5.2 实例属性的查找顺序**
```python
class Person(object):
    """an example class"""
    x = 'abc'  # 类属性
    age = 2
    height = 160

    def __init__(self, name, age=18):
        self.name = name
        self.y = age

    def foo(self):  # 类属性foo，也是方法
        return 'my Class'

    def show(self, x, y):
        self.y = x  # 修改实例属性
        Person.x = x  # 修改类属性


if __name__ == '__main__':
    tom = Person('Tom')  # 实例化、初始化
    jerry = Person('Jerry')
    Person.age = 30
    print(Person.age, tom.age, jerry.age)
    print(Person.height, tom.height, jerry.height)
    Person.height += 20
    print(Person.height, tom.height, jerry.height)
    tom.height += 20
    print(Person.height, tom.height, jerry.height)
    jerry.height = 168
    print(Person.height, tom.height, jerry.height)
```
**执行结果:**
>30 30 30  
160 160 160  
180 180 180  
180 200 180  
180 200 168   

**结论：**  
1. 从执行结果可以推出实例属性的查找顺序：实例tom访问属性，会先找自己的`tom.__dic__`，如果没有，则通过属性`tom.__class__.__dict__`查找自己的类的属性。
2. 如果实例tom通过`tom.__dict__[变量名]`访问属性，则不会按上述查找顺序查找，实例属性没有直接报错。  
3. 实例可以动态的给自己增加一个属性。例如：`tom.x=28`；通过`实例.__dict__[变量名]和实例.变量名`都可以访问属性。  
4. 如果实例tom和类Person都具有同名属性age，则`tom.age`只会访问tom自己的属性。本质上是赋值即定义。  

***约定：类变量使用全大写来命名。***

### 4.4 装饰一个类  
```python
def set_name_property(name):
    def _wrapped(fn):
        print('wrapper {}'.format(fn))
        fn.NAME = name
        return fn
    return _wrapped


@set_name_property('My class')
class Person:
    age = 18

    def __init__(self, age, name):
        self.name = name
        self.age = age

    def __new__(cls, *args, **kwargs):
        print('this is new')
        return super().__new__(cls)

    def show(self):
        print(self.age, Person.age)


if __name__ == '__main__':
    tom = Person('tom', 20)
    print("tom name = {}, Person's name = {}, Person's age = {}".format(
        tom.name, tom.__class__.NAME, tom.__class__.__dict__['age']))
```
**执行结果：**
>wrapper <class '__main__.Person'>  
this is new  
tom name = 20, Person's name = My class, Person's age = 18  

**装饰一个类的作用：** 对于写好的模块，某些特定的场景缺少一个方法或属性，但是又不便于修改已经写好的项目，
可以通过装饰器外部引用，为这个类Class增加需要的属性或方法后，再使用。**本质上是为类对象动态的添加一个属性。**

***
### 4.5 类方法和静态方法

**1. 理解类方法调用过程：**
```python
class MyClass1:
    def foo(self):
        print('foo')

    def bar():
        print('bar')


if __name__ == '__main__':
    a = MyClass1()
    a.foo()
    MyClass1.bar()
    print(MyClass1.__dict__)
    # a.bar()  报错 TypeError: bar() takes 0 positional arguments but 1 was given

```
**执行结果：**  
>foo  
bar  
{'__module__': '__main__', 'foo': <function MyClass.foo at 0x000002A6530A7160>, 
> 'bar': <function MyClass.bar at 0x000002A6530A78B0>, 
> '__dict__': <attribute '__dict__' of 'MyClass' objects>, 
> '__weakref__': <attribute '__weakref__' of 'MyClass' objects>, '__doc__': None}  

**调用过程本质：**  
1. `a.foo()` 调用过程：类的实例a调用与a绑定的类方法foo，python内部将实例a作为位置参数self的实参传入。
2. `MyClass.bar()`调用过程：MyClass从自己的属性`__dict__`中通过`key='bar'`调用function bar。
3. `a.bar()`调用过程：类的实例a调用与a绑定的类方法bar，python内部将实例a作为实参传入，但是类方法bar没有
任何形参，因此报`TypeError: bar() takes 0 positional arguments but 1 was given`。  

**2. 类方法定义：装饰器`@classmethod`**
