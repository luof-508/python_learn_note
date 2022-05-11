# 面向对象(OOP：Object Oriented Programming)9 -- 魔术方法 one more

## 1. `__slot__`:
槽位，槽位数有限。  

字典为了提升查询效率，必须用空间换时间。一般来说一个对象，属性多一点，都存储在字典中便于查询，问题不大。  

假设有一百万个实例，这些实例的属性都放在字典中，消耗内存很大，这个时候怎么办，使用`__slot__`，把属性字典`__dict__`省了，使用`__slot__`规定对象有什么属性。  

**示例：**
```python
class A:
    X = 123
    #  定义了__slots__后，它限定了实例的属性，同时阻止实例产生__dict__, 把__dict__消灭掉。
    #  预测到为了，某个对象可能产生大量的实例，且这个实例有很多不会用到的属性，这个时候就可以用__slot__来暴露需要的属性，节省内存
    #  给出了__slot__后，就无法动态增加属性了。
    __slots__ = 'p1'  # , 'p2'  #  可以是列表、元组，里面放得是字符串名称。但是既然考虑节约内存了，用元组比较好

    def __init__(self):
        self.p1 = 1
        # self.p2 = 2
        pass

    def showme(self):
        print('I am A. {}'.format(self.p1))

        
class B(A):
    pass


if __name__ == '__main__':
    print(A.__dict__)
    # print(A().__dict__)
    a = A()
    print(a.__slots__)
    a.showme()
    # a.p3 = 120  # 给出了__slot__后，就无法动态增加属性了。
    print(a.X)
    # a.X = 1  # 可以吗？赋值即定义，实例不能改变类的属性，是给实例增加属性，所以肯定不可以
    print(B().__dict__)
```
**执行结果：**  
>{'__module__': '__main__', 'X': 123, '__slots__': 'p1', '__init__': <function A.__init__ at 0x0000019007DD9430>, 'showme': <function A.showme at 0x0000019007DD9B80>, 'p1': <member 'p1' of 'A' objects>, '__doc__': None}  
p1  
I am A. 1  
123  
{}  

**小结：** 
- 定义了`__slots__`后，它限定了实例的属性，同时阻止实例产生`__dict__`, 把`__dict__`消灭掉。
- 预测未来某个对象可能产生大量的实例，且这个实例有很多不会用到的属性，这个时候就可以用`__slot__`来暴露需要的属性，节省内存。
- 给出了`__slot__`后，就无法动态增加属性了。
- `__slot__`不影响继承，父类给出了`__slot__`，在子类中不生效，如果子类需要，必须重新定义。

**应用场景：** 需要构造上百万给实例，内存紧张。`free [-hm]`查看内存使用情况

## 2. 未实现和未实现异常
**NotImplemented**： 是一个单值，是<class 'NotImplementedType'>的实例  
**NotImplementedError**： 是一个异常类型   

**示例:**
```python
print(type(NotImplemented))
print(type(NotImplementedError))


class A:

    def show(self):

        #  类设计中，未实现的父类属性，抛一个未实现异常更合适
        raise NotImplementedError
```

## 3. 运算符重载中的反向方法
双目运算符,双目就是两个操作数。  

```python
class B:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):
        print('B add')
        return self.x + other.x

    def __radd__(self, other):  # 反向方法，
        print('B radd')
        return self + other


class C:
    def __init__(self, x):
        self.x = x

    # def __add__(self, other):
    #     print('C add')


class BImprove:
    def __init__(self, x):
        self.x = x

    def __add__(self, other):
        try:
            ret = self.x + other.x
        except AttributeError:
            try:
                ot = int(other)
            except Exception:
                ot = 0  # 根据实际需求，选择不抛异常或抛异常
            ret = self.x + ot
        return ret

    def __radd__(self, other):  # 反向方法
        print('B radd')
        return self + other
    
    def __rsub__(self, other):
        pass
    
    def __rmod__(self, other):
        pass


if __name__ == '__main__':
    b = B(4)
    c = C(5)
    print(b + c)
    # 双目运算符反向加法：对象实例c加号左边，当c的类C中未实现__add__时，解释器尝试调用实例b中的__add__，如果b中实现了__add__，就直接使用
    print(c + b)
    # print(1 + b)  # 报AttributeError: 'int' object has no attribute 'x'。为什么？
    # 实际上，其调用逻辑是：1是int类型，内部实现了__add__方法，但是1 + b，b是B类的实例，int类中实现的__add__无法识别这个实例的类型，于是返回
    # 了NotImplemented单值；解释器发现这是一个值（类似于c + b，从c中没有找到__add__，返回的是None单值）,于是继续发起对第二个对象b的__radd__
    # 方法的调用，对象b实现了__radd__，但数字1没有属性x，所以抛出了AttributeError异常。
    # 解决方案：使用异常捕获处理，类似于int返回NotImplemented。
    print('\~~~~~~~~~~')
    b_im = BImprove(11)
    print(1 + b_im)
    print('abc' + b_im)
    print('5' + b_im)
```
**执行结果：**  
>B add  
9  
B radd  
B add  
9  
\~~~~~~~~~~  
B radd  
12  
B radd  
11  
B radd  
16  

**小结：**  
- 双目运算符反向加法：对象实例c加号左边，当c的类C中未实现__add__时，解释器尝试调用实例b中的__add__，如果b中实现了__add__，就直接使用  
- `1 + b`报AttributeError: 'int' object has no attribute 'x'。为什么？
>实际上，其调用逻辑是：1是int类型，内部实现了__add__方法，但是1 + b，b是B类的实例，int类中实现的__add__无法识别这个实例的类型，于是返回
了NotImplemented单值；解释器发现这是一个值（类似于c + b，从c中没有找到__add__，返回的是None单值）,于是继续发起对第二个对象b的__radd__
方法的调用，对象b实现了__radd__，但数字1没有属性x，所以抛出了AttributeError异常。
