# 面向对象高阶业务运用：检查Person实例的参数类型
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

## 方案一：通过函数实现

检查参数类型，只需写一个check函数，将传入的参数与声明类型进行对比即可达成需求功能。
**代码实现：**
```python
class Person:
    """
    This is Person class
    """
    def __init__(self, name: str, age: int):
        self.check_params([(name, str), (age, int)])
        self.name = name
        self.age = age

    @classmethod
    def check_params(cls, params: list):  # 方案一，写一个check函数。
        for value, typed in params:
            if not isinstance(value, typed):
                raise TypeError(value)
```
**代码分析：** 上述方式，在Person类中侵入了与类业务无关的代码，耦合度太高，大规模项目中，不便于维护。**解决方案：使用装饰器**  

**方案一代码优化：**
```python
def params_assert(cls):
    def wrapper(name: str, age: int):
        """
        This is wrapper
        :param name:
        :param age:
        :return:
        """
        params = [(name, str), (age, int)]
        for value, typed in params:
            if not isinstance(value, typed):
                raise TypeError(value)
            return cls(name, age)
    return wrapper


@params_assert  # 方案一优化，使用装饰器，避免侵入式代码
class Person:
    """
    This is Person class
    """
    def __init__(self, name: str, age: int):
        self.check_params([(name, str), (age, int)])
        self.name = name
        self.age = age
```
**代码分析：** 通过装饰器函数，解决了侵入式代码，将check_params函数与业务类Person解耦。看似完成了缺陷优化，实际上还有问题：wrapper内联函数中params实际上为硬编码，另外装饰后Person变成了函数，还可以进一步优化


## 方案二：使用inspect模块+类装饰器 

**代码实现：**
```python
import inspect


class TypeAssert:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args):
        params = inspect.signature(self.cls)  # 使用inspect模块避免硬编码
        for idx, (name, val) in enumerate(params.parameters.items()):
            if val.annotation != val.empty and not isinstance(args[idx], val.annotation):
                raise TypeError(args[idx])
        return self.cls(*args)


@TypeAssert  # 进一步改造为类装饰器
class Person2:
    """
    This is Person2 class
    """
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


if __name__ == '__main__':
    p = Person2('tom', 18)
    print(p.name, p.age)
    p = Person2('tom', '18')  # 测试异常
```

**上述方案已经很优雅了，还可以使用数据描述器实现**。

##  方案三： 使用描述器 + 类装饰器 + 反射 + inspect模块
**代码实现：**
```python
import inspect


class DateDescriptor3:
    def __init__(self, param, typed=None):
        self.param = param
        self.typed = typed

    def __set__(self, instance, value):
        print('Set Attr', self, instance, value)
        params = inspect.signature(instance.__class__).parameters   # 侵入式代码
        sg = params.get(self.param)
        if sg.annotation != sg.empty and not isinstance(value, sg.annotation):
            raise TypeError(value)
        self.__dict__[self.param] = value

    def __get__(self, instance, owner):
        print('Get Attr', self, instance, owner)
        return self


class Person3:
    """
    This is Person3 class
    """
    name = DateDescriptor3('name')  # 不优雅
    age = DateDescriptor3('age')

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


# 进一步改造为装饰器，解决侵入式代码
# 最终代码：类装饰器 + 反射 + 数据描述器 + inspect
class TypeAssert4:
    def __init__(self, sg_name, sg_annotation):
        self.sg_name = sg_name
        self.sg_annotation = sg_annotation

    def __set__(self, instance, value):
        print('Set Attr', self, instance, value)
        if not isinstance(value, self.sg_annotation):
            raise TypeError(value)
        self.__dict__[self.sg_name] = value

    def __get__(self, instance, owner):
        print('Get Attr', self, instance, owner)
        return self


class DateDescriptorImprove:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args):
        params = inspect.signature(self.cls).parameters
        for idx, (name, sg) in enumerate(params.items()):
            if sg.annotation != sg.empty:  # 当参数有注解时，利用反射设置动态属性，且这个属性为数据描述器
                setattr(self.cls, name, TypeAssert4(sg.name, sg.annotation))
        return self.cls(*args)


@DateDescriptorImprove
class Person4:
    """
    This is Person4 class
    """
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


if __name__ == '__main__':
    p3 = Person3('Jerry', 19)
    print(p3.name.__dict__['name'], p3.age.__dict__['age'])
    print('~~~~~~~~~~~~~~')
    # Person3('jerry', '19')  # 异常测试
    print('~~~~~~~~~~~~~~')
    p4 = Person4('David', 19)
    print(p4.name.__dict__['name'], p4.age.__dict__['age'])
    Person4('David', '20')  # 异常测试
```
