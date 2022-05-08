## 十三、python的魔术方法  

**魔术方法是其他语言没有的方法，能够大大提高编程效率，更加pythonic**  

### 13.1 对象的特殊属性

|名称|含义|说明|  
|:-:|:-:|:-|  
|`__name__`|类、函数、方法等的名字|实例没有
|`__module__`|类定义所在的模块名|序列化的时候会记住module，一个module可以认为是一个名词空间  
|`__bases__`|类的基类的元组|`__bases__`不是mro，只是基类列表中的按顺序出现的一个列表  
|`__mro__`|类的mro，多继承的属性查找顺序|class.mro()返回的结果保存在`__mro__`中  
|`__dict__`|类或实例的属性，可读写的字典  
|`__class__`|对象或类的所属类  
|`__doc__`|类或函数的文档字符串，如果没有定义则为None|  


### 13.2 查看属性dir()  
|方法|意义|  
|:-:|:-|  
|`__dir__`|返回类或对象的所有成员名称列表。内建函数dir(obj)就是调用`obj.__dir__()`。如果obj提供`__dir__()`则调用之，否则会尽量从obj的`__dict_`_属性中收集信息, dir()详细说明可追源码。  

**示例：**  
```python
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
        return ['Cat']


if __name__ == '__main__':
    ha = Dog('ha')
    cat = Cat('Gard')
    print(dir(Animal))
    print(dir(Dog))
    print(dir(ha))
    print(ha.__dir__())
    print(dir(Cat))
    print(dir(cat))
    print(dir())
    print(set(list(ha.__dict__.keys())) | set(list(ha.__class__.__dict__.keys())) | set(list(object.__dict__.keys())))
```
**从示例执行结果可以看出：** 
1. 对象Dog未定义属性`__dir__`时，`dir(Dog)`或`dir(ha)`，相当于先查找对象自己的`__dict__`->再查找对象的类的`__dict__`->再查找基类的`__dict__`;
所以，除几个特色属性外，几乎等价于最后一行方法
2. 对象Cat定义了`__dir__`时，执行`dir(cat)`,直接调用实例的`__dir__`方法。注意：**自定义`__dir__`时最好返回list**  
3. **import modulename，导入的是名词空间**  

### 13.3 魔术方法  

**分类：**  
- 创建与销毁：`__init`,`__new__`，`__del__`  
- hash：`__hash__`
- bool：`__bool__`
- 可视化：`__repr__`,`__str__`
- 运算符重载：
- 容器和大小：
- 可调用对象：
- 上下文管理：
- 反射：
- 描述器：
- 其他杂项：

#### 13.3.1 创建与销毁  
`__new__`构建实例，不管什么语言，一般不要乱动；`__del__`，对象销毁的时候调用，实际用处很少。  

**创建与销毁的的对象模型：**  
&emsp;&emsp;构建实例，就是类作为一个模板，利用这个模板在内存中创建出一个跟类相关的实例，而这个实例会在内存中占一块地方用于存储类的相关属性，
python存放相关属性用字典管理`__dict__`，从而建立了一个名称与对象的映射关系，相当于构建了一张表方便查询。 
实例放在内存中，它的属性值在内存中是散落的，建立字典`__dict__`便于管理或者统一管理。
实例构建完之后，马上进行初始化`__init__`，因为`__new__`只是照着类模板构建了实例，但是实例还没有自己个性化的属性，怎么办，添呗，
就用初始化函数`__init__`， 把个性化的东西放在实例的`__dict__`中，方便查阅，实际上在内存中也是散落的。

**注意：** 初始化函数`__init__`如果要return，只能return None  


#### 13.3.2 hash与去重：`__hash__ ` 
|名称|含义|说明|  
|:-:|:-:|:-|  
|`__hash__`|内建函数hash(obj)调用的返回值，返回一个整数。如果对象obj中定义了这个方法，这个对象的实例就是可hash的。  
|`__eq__`|对应`==`操作符，判断2个对象是否相等，返回bool值  

hash默认是对内存中的地址求hash值。hash原理都是一样，用取模法去理解hash算法,那些一系列的复杂算法，不过就是让冲突域更大，冲突的可能性更小。  
hash一定会有冲突，不可避免。hash值相同不代表两个对象是同一个东西，因此去重和hash是两回事。hash值相同，去重还要看值等不等。  

**示例：**
```python
from  collections import Hashable
class A:
    X = 123

    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __hash__(self):  # 不同实例hash冲突示例
        # __hash__必须返回一个整型
        return 12

    def __eq__(self, other):  # 为什么需要相等函数
        # 分别注释掉本方法和不注释执行看看去重结果差异
        return self.y == other.y


def hash_(x):
    return x % 3


if __name__ == '__main__':
    print(hash(A(5, 7)))
    print(isinstance(A, Hashable))
    a = A(5, 7)
    b = A(5, 7)
    print(a, b)
    print(a is b)
    # python实现二元操作符等价为一个方法的原理，如操作符`==`:
    print(a==b) # 等价于a.__eq__(b)
    s = {a, b}
    print(s)
```
**未注释`__eq__`执行结果**：  
>12  
<__main__.A object at 0x000002340DD311F0> <__main__.A object at 0x000002340DD312E0>  
False  
{<__main__.A object at 0x000002340DD311F0>}  

**小结：** 注释掉Class A中的`__eq__`执行去重实例a,b，和不注释`__eq__`，再执行去重。
从两次执行结果可以看出，**set去重，默认先执行is,判断两个实例在内存中是不是同一个东西,后找==**；
如果要自定义去重方法，需要在对象中提供`__eq__`方法，这个时候去重则直接根据`__eq__`的结果进行处理。

**hash与去重总结：**
- 一个对象定义了`__hash__`方法，就代表这个对象的实例可hash，但可hash，且hash值相等，不代表可去重。
- hash和去重是两回事。去重set默认比较内存中两个对象是不是同一个东西，即做is，然后才做== 
- 通过list的原码可知，设计不可hash对象，定义对象属性`__hash__ = None`即可
- `__hash__`方法只是返回一个hash值作为set或者dict的key，可hash对象必须提供`__hash__`方法
- 判断一个对象是否可hash，使用`collections.Hashable`。例如：`isinstance(a, Hashable)`。
- python实现二元操作符等价为一个方法的原理就是利用`__eq__`等魔术方法，如操作符`==`:`print(a==b) # 等价于a.__eq__(b)`  
- hash：hash散列，如MD5。**hash一般用在缓存的时候，提高检索或查询的速度。时间复杂度0(1)。**

#### 13.3.3 布尔：`__bool__`  
内建函数bool(obj)或者obj放在逻辑表达式位置时，首先调用的就是对象的`__bool__`方法，返回对象的bool值。 
```python
class P:
    def __init__(self, x):
        self.x = x

    def __len__(self):
        return len(self.x)

    def __bool__(self):
        return False

```
**bool(obj)执行逻辑：** 如果obj没有定义`__bool__`，就找obj的`__len__`；如果`__len__`也没有定义，那么所有实例都返回为真。
- list、set、dict等内置数据结构为空时，等效为False，原因就是定义了`__len__`魔术方法  
- **所以容器类型的往往不会实现`__bool__`方法，而会实现`__len__`方法**  

#### 13.3.4 可视化：`__repr__`，`__str__`，`__bytes__`  
|名称|含义|说明|  
|:-:|:-:|:-|  
|`__repr__`|执行内建函数repr(obj)时，就是调用`obj.__repr__()`,如果没有定义`__repr__`，则返回对象在内存中的地址。|  
|`__str__` |执行内建函数str(obj)、format(obj)、print(obj)，首先调用`obj.__str__()`；如果没有定义`__str__`,则调用`obj.__repr__()`；如果`__repr__`也没有定义，则返回对象在内存中的地址。|  
|`__bytes__`|执行内建函数bytes(obj)时，就是调用`obj.__bytes__()`，如果没有定义，抛错|  

**示例：**
```python
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

    def __len__(self):
        return 1

    def __bool__(self):
        return False

    def __repr__(self):
        return 'abc'

    def __str__(self):
        return '123'

    def __bytes__(self):
        return b'def'


if __name__ == '__main__':
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1 == p2)
    print(p1)
    print(p2)
    lst = [p1, p2]
    print(lst)
    print(*lst)
    print(list(map(str, lst)))
    print(bytes(p1))  # 注释掉`__bytes__`将抛错
```
**执行结果：**
>False  
123  
123  
[abc, abc]  # print(lst)打印结果，原因为print函数调用的是list的`__str__`
123 123  
['123', '123']  
b'def'  

**应用场景**：当在使用str(obj)这种函数直接对一个对象obj取字符串表达的时候，就是调用对象的的可视化魔术方法，format、print方都是调用可视化模式方法。  
**调用逻辑**： 内建函数str(obj)、format(obj)、print(obj)，首先调用对象`obj.__str__()`；如果没有定义`__str__`,则调用`obj.__repr__()`；
如果`__repr__`也没有定义，则返回对象在内存中的地址。
- print([obj，obj])的时候，如果obj中没有定义`__repr__`，则返回内存中的地址。因此如果要保证什么情况下都能呈现想呈现的东西时，至少给出`__repr__`。

#### 13.3.5 运算符重载  
operator模块提供以下特殊方法，这些特殊方法，都可以通过运算符重载，将类的实例使用这些操作符来操作。
|运算符|特殊方法|含义|  
|:-:|:-:|:-|  
|`<,<=,==,>,>=,!=`|`__lt__,__le__,__eq__,__gt__,__ge__,__ne__`|比较运算符|  
|`+,-,*,/,%,//,**,divmod`|`__add__,__sub__,__mul__,__truediv__,__mod__,__floordiv__,__pow__,__divmod`|算数运算符，移位、位运算也有对应的方法|  
|`+=,-=,*=,/=,%=,//=,**=`|`__iadd__,__isub__,__imul__,__itruediv__,__imod__,__ifloordiv__,__ipow__`|  

**比较运算符运用示例：** 
```python
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


if __name__ == '__main__':
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    print(p1 == p2)
    print(p1 + p2)  # 相比通过加法函数相加print(p1.add(p2))，运算符重载更符合相关专业人士的使用习惯
```
**示例小结：** 坐标类Point，通过重载比较运算符`==`，实现大小比较，不给出`__eq__`的话，就调用Object的。
通过定义`__add__`方法，重载加法运算符+，比直接提供加法add更加适合该领域内使用者的习惯。**运算符重载最好的示例：`pathlib.Path()/'a'/'b'`**
很多内建类型都给出了重载运算方法，比如内建函数int，几乎实现了所有操作符重载的魔术方法，需要的时候可以看源码参考，也可以看帮助文档。  

**应用场景：** 主要运用于面向对象实现的类，需要做大量运算的场景，运算符是这种运算在数学上最常见的表达式。比如实现Point类相加的二元操作：`Point + Point`。
所以**好的类的设计，有运算需求，就应该提供运算符重载**。  

**比较操作符练习**:
```python
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
```

#### 13.3.6 容器相关方法  
|方法|含义|  
|:-:|:-|  
|`__len__`|长度。内建函数len(obj)，调用的就是`obj.__len__()`。如果没有提供将抛错，其实就是把对象当做容器类型看，就如同list或dict。bool()函数调用的时候，如果没有`__bool__`，就会看有没有`__len__`。注意有些第三方库len和size不是一个动作，size指的是内存中有多少个格子存放东西，而len才指元素的个数。  
|`__iter__`|迭代。迭代容器时调用，返回一个新的迭代器对象。因此给出`__iter__`时，必须return一个迭代器。迭代很重要，很多时候，关心的容器能不能迭代，有没有我想要的东西在里面。|  
|`__contains__`|in成员运算符。不同容器有不同实现方法，比如列表，就一个一个找，字典求hash速度很快；所以可以不提供，不提供就调用`__iter__`方法遍历。|  
|`__getitem__`|实现`self[key]`访问。注意不仅限于dict，不要被key迷惑，列表，元组都可以，这个时候key就是索引。所以：对于序列对象(例如购物车类Cart),key接受整数为索引，或者切片(可见，切片调用的就是`__getitem__`)；对于set或dict，key为hashable。key不存在引发keyError异常。|  
|`__setitem__`|与`__getitem__`类似，就是根据中括号给的索引或者给的key，然后找到置，把值塞进去。对于序列对象key超界，引发IndexError。|  
|`__missing__`|对于dict/set类型对象，调用`__getitem__`，但塞进去的是一个不存在的key，通过`__missing__`处理修正|  

**电商购物车通过运算符重载以及容器类操作，实现增加、迭代商品等更方便的操作示例**：
```python
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


if __name__ == '__main__':
    car = Cart()
    print(car + Item('item1', 12) + Item('item2', 1) + Item('item3', 8))  # 链式编程加法，等价于:
    # car.__add__(Item('item1', 12)).__add__(Item('item2', 1)).__add__(Item('item3', 8))
    print(len(car))  # 长度
    for x in car: print(x)  # 迭代，相比取self.items进行迭代，没有把属性暴露出去，更好
    print(car[2])  # 索引操作，调用__getitem__
    car[2] = Item('item_x', 58)  # 调用__setitem__
```  

#### 13.3.7 可调用对象:`__call__`
**可调用对象：** 定义一个类，并实例化得到其实例，将实例像函数一样调用。  
python中一切皆对象，函数也不例外，例如：
```python
def foo():
    print(foo.__module__, foo.__name__)
foo()  # 等价于foo.__call__()
```
|方法|意义|说明|    
|:-:|:-:|:-|  
|`__call__`|类中定义一个`__call__`,类的实例就可以像函数一样调用|对象obj加上()，就是调用对象的`__call__()`方法。obj()等价于`obj.__call__()`。|  

**示例：定义一个斐波那契数列的类，方便调用，并计算第n项**
```python
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
    f = Fib()
    print(f(1))
    print(f(2))
    print(f(5))
    print(f(8))
    print(f[8])
```
**示例小结：** 通过类及魔术方法实现斐波那契数量，实现缓存，便于检索  


#### 13.3.8 上下文管理`__enter__`，`__exit__`
文件IO操作可以使用`with...as`语法对文件对象进行上下文管理。python通过魔术方法，将类实现得较为复杂，但是使用者用着特别方便，比如可以把一个自定义类变成上下。
|方法|意义|说明|    
|:-:|:-:|:-|  
|`__enter__`|进入与对象相关的上下文。一个对象中该方法存在，则with语句会把该方法的返回值绑定到as子句中指定的变量上|**上下文管理前提是，必须写在一个类上，然后在实例上执行**|  
|`__exit__(self, exc_type, exc_val, exc_tb)`|退出与对象相关的上下文。|`exc_type, exc_val, exc_tb`是三个与异常相关的参数。<br>`exc_type`：异常类型，<br>`exc_val`：异常的值，<br>`exc_tb`：异常的追踪信息traceback。 <br>如果上下文退出时没有异常，则这3个参数都为None；如果有异常，退出上下文同时抛出异常，`__exit__`如果return一个等效的True，则压制异常不会抛出。|  

**示例：**
```python
import sys


class Point:
    def __init__(self):
        print('init')

    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')


if __name__ == '__main__':
    p = Point()
    with p as f:
        # sys.exit()  # 测试异常退出python环境，会不会执行__exit__
        print(f == p)
        print('with...as')
```
**执行结果**
>init  
enter  
True  
with...as  
exit  

**小结：**   
- 通过with开启一个上下文运行环境，可以在执行前进行一些预加载或预处理工作，执行后执行收尾的工作；
- 上下文管理方便且安全，哪怕是退出python环境，也会执行`__exit__`语句；  
- 类的上下文管理中，with语句会把`__enter__`方法的返回值绑定到as子句中指定的变量上f。**上下文管理必须写在一个类上，然后在实例上执行** 

**异常测试：**
```python
class E:
    def __init__(self):
        print('init')

    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')
        # return True  # `__exit__`如果return一个等效的True，则压制异常不会抛出

if __name__ == '__main__':
    with E() as f:
        raise Exception('This is exception.')
        print('test exception')
```
**执行结果：**  
>Traceback (most recent call last):    
  File "***.py", line 66, in <module>  
    raise Exception('This is exception.')  
Exception: This is exception.   

**小结：** `__exit__`如果return一个等效的True，则压制异常不会抛出。

**上下文管理和类装饰器：** 上下文管理，也可以像装饰器一样，实现前后的功能增强；装饰器高级玩法--类装饰器，类装饰器是借助`__call__`魔术方法实现的，注意区分类装饰器和装饰一个类。

**示例：** 通过类装饰器，装饰加法函数add，测试函数执行时间，同时实现类装饰器的上下文管理
```python
import datetime
import functools
import time


class Add:
    """
    This is Add class
    """
    def __init__(self, fn):
        self._fn = fn
        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        print('__call__ start')
        ret = self._fn(*args, **kwargs)
        print('__call__ end')
        return ret

    def __enter__(self):
        self.start = datetime.datetime.now()
        print('Context wrapper: __enter__, time={}'.format(self.start))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.total = (datetime.datetime.now() - self.start).total_seconds()
        print('Context wrapper: __exit__, exit time={}'.format(self.total))


def time_it(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        """
        This is wrapper
        :param args:
        :param kwargs:
        :return:
        """
        start = datetime.datetime.now()
        print('wrapper start, time={}'.format(start))
        ret = fn(*args, **kwargs)
        print('ret={}'.format(ret))
        total = (datetime.datetime.now() - start).total_seconds()
        print('wrapper end, exe time={}'.format(total))
        return ret
    return wrapper


@Add
@time_it  # 等价式：aa=time_it(add) -> a=Add(aa)-> a.__enter__()-> a.__call__(1,2) -> a.__exit__()
def add(*args, **kwargs):
    """
    This is add function
    :param args:
    :param kwargs:
    :return:
    """
    time.sleep(0.5)
    return sum(args) + sum(kwargs.values())


if __name__ == '__main__':
    # add(1, 2)
    # print(add.__doc__, type(add))
    with add as f:
        print('context ret={}'.format(f(2, 3)))
```  
**执行结果：**  
>Context wrapper: __enter__, time=2022-04-29 22:06:39.894016  
__call__ start  
wrapper start, time=2022-04-29 22:06:39.894016  
ret=5  
wrapper end, exe time=0.500204  
__call__ end  
context ret=5  
Context wrapper: __exit__, exit time=0.500204  

**小结：**      
- 装饰器，把跟业务无关的函数都抽象出去，实现非侵入式编程风格。  
- 通过类装饰器+上下文管理，避免侵入式代码的同时，不需要多重装饰器，实现更加丰富的功能：通过方法的封装，在执行前进行预加载，比如连接数据库、网络客户端请求等等；执行后保证关闭，出问题保证清理工作。  
- 多个装饰器，可以通过装饰器的等价式，理解装饰器的调用顺序：`aa=time_it(add) -> a=Add(aa)-> a.__enter__()-> a.__call__(1,2) -> a.__exit__()`。  

**上下文应用场景：** 
1. 增强功能：在代码执行前后增加代码，以增强功能。类似装饰器的功能
2. 资源管理：打开了资源需要关闭，例如文件对象、网络连接、数据库连接等
3. 权限验证：在执行代码之前，做权限验证，在`__enter__`中处理


#### 13.3.9 `@contextlib.contextmanager`装饰器  

对于单值生成器函数，即只yield 1个值时，可使用contextmanager装饰器，实现上下文管理，将yield返回值与as子句后面的变量绑定，并执行完yield后面的函数语句
```python
import contextlib


@contextlib.contextmanager  # 不使用此装饰器时，不会执行exit函数语句
def foo():
    print('enter')
    yield 123
    print('exit')  # 异常情况，不能保证exit语句执行，使用try...finally语句


def foo1():
    print('enter')
    try:
        yield 123
    finally:
        print('exit')  


@contextlib.contextmanager
def foo2():
    for i in range(3):  # yield不止1个值时，将抛RuntimeError: generator didn't stop异常
        yield i


if __name__ == '__main__':
    # next(foo())
    with foo() as f:
        print(f)

    with foo2() as f:
        print(f)
```
**小结：** 对于业务逻辑较为复杂的场景，直接使用`__enter__`、`__exit__`方法更可靠。  

#### 13.3.10 `@functools.total_ordering`装饰器  

比较运算符`<、>、<=、>=`如果每一个都在类中实现太麻烦了，通过total＿ordering装饰器，只需要在类中实现`<、>、<=、>=`中的任意一个，即可进行实例的相关比较。
```python
import functools


@functools.total_ordering
class A:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return self.x == other.x

    def __gt__(self, other):
        return self.x > other.x


if __name__ == '__main__':
    a1 = A(3)
    a2 = A(4)
    a3 = A(3)
    print(a1 == a2)
    print(a1 > a2)
    print(a1 <= a2)
    print(a1 == a3)
```
**小结**：
- 从执行示例可以看出：注释`__eq__`方法后，`a1==a2`返回值为false，与预期不符。这与前述去重吻合：当没有给出`__eq__`时，判断例是否相等，默认比较内存中的id。  
- 所以`==`必须单独实现，否则比较结果不准确  


#### 13.3.11 反射  
概念：**运行时**，指程序被加载到内存中执行的时候。区别于编译时。
**反射**：reflection，指运行时获取类型定义信息。一个对象能够在运行时，像照镜子一样，反射出其类型信息就是反射。简单的说，在python中，能够通过一个对象，找出其type、class、attribute或method的能力，称为反射。
例如：Point类的实例p，通过反射能力，在`p.__dict__`中找到自己的attribute，并且修改、增加自己的attribute。**通过`__dict__`获取、修改属性不优雅，python提供了内建函数：**  
|方法|意义|说明|    
|:-:|:-:|:-|  
|`getattr(object, name[, default])`|通过name返回 object的属性值。属性不存在返回default，如果没有给出default，抛AttributeError。|注意，name必须为字符串类型；<br>getattr搜索顺序，遵从mro搜索顺序，先从自己的`__dict__`中找，然后找class的...|  
|`setattr(object, name, value)`|object的属性存在则覆盖，不存在新增。|注意：object为类则新增类属性，为实例则新增实例性。<br>--动态增加属性，未绑定。增加到实例，则在实例的__dict__中。|  
|hasattr(object, name)|判断对象是否有这个名字的属性|name必须为字符串类型  

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    p = Point(2, 3)
    # 运用对象的反射能力，在`p.__dict__`中找到自己的attribute，并且修改、增加自己的attribute
    print(p.__dict__)
    p.__dict__['x'] = 3
    p.z = 12
    print(p.__dict__)
    # 通过反射能力，在`p.__dict__`中找到自己的attribute，并且修改、增加自己的attribute
    setattr(Point, 't', 14)
    print(p.__dict__)
    print(getattr(p, 't'))
    if not hasattr(p, 'lab'):
        setattr(p, 'lab', lambda x: print(x))
        setattr(Point, 'lab1', lambda self: print('lab1'))
    print(p.__dict__)
    print(Point.__dict__)
    p.lab('lab')
    p.lab1()
```
**执行结果**: 
>{'x': 2, 'y': 3}  
{'x': 3, 'y': 3, 'z': 12}  
{'x': 3, 'y': 3, 'z': 12}  
14  
{'x': 3, 'y': 3, 'z': 12, 'lab': <function <lambda> at 0x000001D3B1129430>}  
{'__module__': '__main__', '__init__': <function Point.__init__ at 0x000001D3B1129160>, '__dict__': <attribute '__dict__' of 'Point' objects>, '__weakref__': <attribute '__weakref__' of 'Point' objects>, '__doc__': None, 't': 14, 'lab1': <function <lambda> at 0x000001D3B1129940>}  
lab  
lab1  

**小结**：动态增加属性的方式，和装饰器修饰一个类、Mixin方式的差异在于，Mixin和装饰器在编译时就决定了；而动态增、删属性的方式是运用反射能力，运行时改变类或实例的属性，更灵活。
**练习：** 通过`getattr/setattr/hasattr`改造命令分发器
```python
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
    dis = Dispatcher()
    dis.reg('cmd1', lambda self: print('cmd1'))
    dis.reg('cmd2', lambda self: print('cmd2'))
    dis.run()
```


**反射相关的魔术方法：`__getattr__、__setattr__、__hasattr__`**  
|方法|意义|说明|    
|:-:|:-:|:-|  
|`__getattr__`|当通过搜索实例、实例的类及祖先类查找不到属性时，就会调用此方法；如果没有这个方法，就会抛AttributeError异常  
|`__setattr__`|通过`obj.x=100`方式增加、修改实例的属性都要调用`__setattr__`，包括初始化函数中的实例属性赋值  
|`__delattr__`|通过实例来删除属性时调用此方法，可以阻止通过实例删除属性的操作。但是通过类依然可以删除属性  
|`__getattribute__`|实例所有的属性调用都从这个方法开始，它阻止了属性的查找；该方法应该返回一个值或者抛出AttributeError.<br>如果return值，则作为属性的查找结果；如果抛出AttributeError，则会直接调用`__getattr__`方法，表示没有找到属性。<br>除非明确知道`__getattribute__`用来做什么，否则不要使用此方法  


**示例1：**
```python
class Base:
    n = 0


class Point(Base):
    z = 6

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getattr__(self, item):
        return 'missing {}'.format(item)

    def __setattr__(self, key, value):
        print('setattr')
        # self.__dict__[key] = value


if __name__ == '__main__':
    p1 = Point(1, 2)
    print(p1.x)
    print(p1.z)
    print(p1.n)
    print(p1.t)  # missing t
```
**执行结果：**
>setattr  
setattr  
missing x  
6  
0  
missing t  

**小结：** 
- 示例中给出了`__setattr__`方法，因此在类初始化时，设置实例属性调用了此方法，但是`__setattr__`中没有完成实例`__dict__`的操作，所以实例`__dict__`没有属性x、y；通过`p1.x`访问实例属性x，才调用了` __getattr__`。
- 因此：`__setattr__`方法，可以拦截对实例属性的增加、修改操作；如果给出了这个方法，要想增加、修改实例属性生效，必须在方法中实现`__dict__`操作。  

**示例2：**
```python
class P:
    Z = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __delattr__(self, item):
        print('can not delete {}'.format(item))


if __name__ == '__main__':
    p2 = P(4, 5)
    del p2.x
    p2.z = 13
    del p2.z
    del p2.Z
    print(p2.__dict__)
    print(P.__dict__)
    del P.Z
    print(P.__dict__)
```
**执行结果：**
>can not delete x  
can not delete z  
can not delete Z  
{'x': 4, 'y': 5, 'z': 13}  
{'__module__': '__main__', 'Z': 4, ...}
{'__module__': '__main__', '__init__': <function P.__init__ at 0x000002349845DAF0>, ...}

**小结：** `__delattr__`方法，可以阻止通过实例删除属性的操作。但是通过类依然可以删除属性。

**示例3：**
```python
class Base:
    n = 0

    
class C(Base):
    C = 8

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getattr__(self, item):
        return 'missing {}'.format(item)

    def __getattribute__(self, item):
        # raise AttributeError
        return 'getattribute:{}'.format(item)


if __name__ == '__main__':
    c = C(3, 4)
    print(c.__dict__)
    print(c.x)
    print(c.c)
    print(c.n)
    print(C.__dict__)
    print(C.C)
```
**执行结果：**
>getattribute:__dict__  
getattribute:x  
getattribute:c  
getattribute:n  
{'__module__': '__main__', 'C': 8, '__init__': <function C.__init__ at 0x00000177F7A1DCA0>, '__getattr__': <function C.__getattr__ at 0x00000177F7A1DD30>, '__getattribute__': <function C.__getattribute__ at 0x00000177F7A1DDC0>, '__doc__': None}  
8  

**小结：**
- 实例的所有属性访问，第一个都会调用`__getattribute__`方法，它阻止了属性的查找；该方法应该返回一个值或者抛出AttributeError.如果return值，则作为属性的查找结果；如果抛出AttributeError，则会直接调用`__getattr__`方法，表示没有找到属性。
- 除非明确知道`__getattribute__`用来做什么，否则不要使用此方法

**总结：** 属性的查找顺序：实例调用`__getattribute__() -> instance.__dict__ -> instance.__class__.__dict__ -> 继承的祖先类的__dict__ ->调用__getattr__()`


#### 13.3.12 描述器：`__get__、__set__、__delete__`

**描述器：** 当类的定义中实现了`__get__、__set__、__delete__`三个魔术方法中的任意一个时，那么这个类就是一个描述器
- 当仅实现了`__get__`，称为**非数据描述器non data descriptor**;
- 当同时实现了`__get__` + `__set＿`或`__delete__`就是**数据描述器data descriptor**  

**owner属主：** 如果一个类的类属性包含描述器，那么这个类称为owner属主

常见的数据描述器：property


1. 描述器通过`__get__`方法，对类的实例读取类属性的控制：

`__get___(self, instance, owner)`方法:  
- instance：属主的实例，当通过类B的实例b读取属性x时，解释器自动传入b和B
- owner：属主，当通过类B读取属性x时，instance为None，只传入B  

**示例：**
```python
class A:
    AA = 'aa'

    def __init__(self):
        print('A.init')
        self.a1 = 'a1'

    def __get__(self, instance, owner):
        print('A:__get__', self, instance, owner)
        return self  # 通常return self


class B:
    x = A()

    def __init__(self):
        print('B.init')
        # self.x = 100
        self.y = A()

        
if __name__ == '__main__':
    print(B.x)
    print(B.x.AA)  # 通过类B读取类属性x，因为x是一个描述器，触发__get__
    print('~~~~~~~~~~')
    b = B()
    print(b.x.AA)  # 通过类B的实例b读取类属性x，因为x是一个描述器，触发__get__
    print('~~~~~~~~~~')
    print(b.y.a1)  # 通过实例属性访问类A的实例的属性，不会触发__get__
```
**小结：**  
- 当类A的实例x是类B的属性时，如果类A中给出了`__get__`方法，则对类B属性x的读取（不管是通过B的实例或B），或者进一步通过属性x访问类A的属性，都会触发`__get__`方法；所以一般`__get__`方法返回self。
- 当类A的实例是类B的实例的属性时，通过类B的实例属性访问类A的实例的属性的时候，不会触发`__get__`方法

2. 数据描述器通过`__set__`或者`__delete__`方法，对类的实例修改类属性的控制：
**示例：**
```python
class C:
    CC = 'cc'

    def __init__(self):
        print('C.init')
        self.c1 = 'c1'

    def __get__(self, instance, owner):
        print('C:__get__', self, instance, owner)
        return self  # 通常return self

    def __set__(self, instance, value):
        print('C:__set__', self, instance, value)


class D:
    x = C()

    def __init__(self):
        print('D.init')
        self.x = 100
        self.y = 123


if __name__ == '__main__':
    print('-----------')
    print(D.x)
    d = D()
    print(d.__dict__)  # 查看实例d的__dict__是否有属性x
    print(D.__dict__)
    print('~~~~~~~~~~~~~~')
    print(d.x)
    d.x = 100    # 尝试为实例d增加属性x
    print(d.x)   # 查看‘赋值即定义’是否可以增加实例属性x。从结果可以看出，由于类属性x是数据描述器，由于受数据描述器拦截，无法给实例d的__dict__写入x,即增加x属性。
    print(d.__dict__)
    print('~~~~~~~~~~~~~')
```
**小结**： 
- 当类D中存在一个标识符为x的类属性，且这个属性x为数据描述器时，则这个类属性x在类D的__dict__的优先级高于类D的实例__dict__的优先级；即通过类D的实例d进行访问、修改属性x操作时（d.x或d.x=100），优先访问`D.__dict__`。
- 所以，**一但类属性x为数据描述器，则实例b只能操作类属性x，无标识符为x的实例属性**；而操作类属性x又受描述器控制，才会有`d.x=100`时触发了数据描述器的`__set__`方法，有点像运算符重载`d.x=100 -> d.x.__set__(d, 100)`。
- 本质上：数据描述器`d.x=100 -> d.__dict__.get(x) -> d.__dict__没有x，继续找类的__dict_ ->d.__class__.__dict__[x] -> 找到了，但是x是描述器，类似运算符重载 -> d.__class__.__dict__[x].__set__()`，走不到写`d.__dict__`的操作；`d.x`也是一样，从自己的`__dict__`中找不到x，就找类的，而类属性x又是一个描述器，进而触发了`__get__`.

**总结：** python的方法几乎都实现为非数据描述器（例如staticmethod、classmethod），因此实例可以重新定义一个标识符与类属性一样的实例属性，从而允许单个实例可以获得与同一类的其他实例不同的行为。property函数实现为一个数据描述器，因此被property装饰的类属性z，实例无法定义一个同为标识符z的实例属性。
**示例：**
```python
class E:
    
    @classmethod
    def foo(cls):
        pass
    
    @staticmethod
    def bar():
        pass
    
    @property
    def z(self):
        return 2
    
    def __init__(self):
        self.foo = 100  # foo和、bar方法都为非数据描述器，所以可以直接赋值修改
        self.bar = 123
        self.z = 'z'  # z方法为数据描述器，不能在实例中替换
```

**练习：实现classmethod和staticmethod**
```python
import functools


class ClassMethod:
    def __init__(self, fn):
        print(fn)
        self._fn = fn

    def __get__(self, instance, owner):
        print(self, instance, owner)
        # return self._fn(owner)
        return functools.partial(self._fn, owner)


class StaticMethod:
    def __init__(self, fn):
        print(fn)
        self._fn = fn

    def __get__(self, instance, owner):
        print(self, instance, owner)
        return self._fn


class A:

    @StaticMethod  
    def foo():
        print('static')

    @ClassMethod  # foo = ClassMethod(foo) -> 新的foo是类ClassMethod的实例， 而ClassMethod非数据描述器，故通过A.foo读取类属性foo时，触发调用__get__，而__get__返回的是固定了参数cls的新的foo。所有最后可以直接foo()执行函数。
    def bar(cls):
        print(cls.__name__)


if __name__ == '__main__':
    f = A.foo
    print(f)
    f()
    b = A.bar
    print(b)
    b()
```
