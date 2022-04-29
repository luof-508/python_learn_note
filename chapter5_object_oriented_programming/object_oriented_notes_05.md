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
- python实现二元操作符等价为一个方法的原理就是利用`__eq__`，如操作符`==`:`print(a==b) # 等价于a.__eq__(b)`  
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
|`__liter__`|迭代。迭代容器时调用，返回一个新的迭代器对象。因此给出`__liter__`时，必须return一个迭代器。迭代很重要，很多时候，关心的容器能不能迭代，有没有我想要的东西在里面。|  
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


#### 13.3.8 可调用对象上下文管理：`__enter__`，`__exit__`：
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
