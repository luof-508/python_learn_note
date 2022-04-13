# 面向对象OOP：Object Oriented Programming

## 5 访问控制  
### 5.1 私有属性(Private)和保护变量(Protected)
**示例：** 设计一个实例的私有属性`__age`，外部不能直接访问或修改这个属性，调用`age_up`符合控制逻辑，属性`__age`才能被修改,只能通过`get_age`访问属性`__age`。
```python
class Person1:
    def __init__(self, name):
        self._name = name  # 保护变量，内部函数或内部变量，不要引用
        self.__age = 18  # 私有属性

    def age_up(self, num: int):
        if 0 < self.__age < 150:  # 控制逻辑
            self.__age += num

    def get_age(self):
        return self.__age


if __name__ == '__main__':
    tom = Person1('tom')
    print(tom.__dict__)
    print(tom._Person1__age)
    tom._Person1__age = 180
    tom.__age = 100
    print(tom.__dict__)
    tom._name = 'jerry'
    print(tom.__dict__)
```
**执行结果：**
>{'_name': 'tom', '_Person1__age': 18}  
18  
{'_name': 'tom', '_Person1__age': 180, '__age': 100}  
{'_name': 'jerry', '_Person1__age': 180, '__age': 100}  

**总结：**
- **私有属性，** 本质是类定义的时候，如果声明了一个实例变量的时候，使用双下划线，python解释器会将其改名，转换为`_类__变量名`的名称。
而在实例化后，动态赋值的属性，比如`tom.__age=100`，非类定义的时候，解释器不会改名。
- **保护变量：** 和普通属性一样，解释器不做任何特殊处理，只是开发者的共同约定，看见这种变量，就如同私有变量，不要直接使用。 
- 知道私有属性的新名称后，外部也可以绕过直接访问、修改。


### 5.2 私有方法  
**示例：**
```python
class Person:
    def __init__(self, name):
        self._name = name  # 保护变量，内部函数或内部变量，不要引用
        self.__age = 18  # 私有属性

    def age_up(self, num: int):
        if 0 < self.__age < 150:
            self.__age += num

    def get_age(self):
        return self.__age

    def __growup(self, incr=1):
        if 0 < incr < 150:
            self.__age += incr


if __name__ == '__main__':
    # 私有方法
    tom = Person('tom')
    tom._Person__growup()
    print(tom.__dict__)
    print(tom.__class__.__dict__)

```
**执行结果：**  
>{'_name': 'tom', '_Person__age': 19}  
{'__init__': <function Person.__init__ at 0x000001C4D90E7160>, 
'age_up': <function Person.age_up at 0x000001C4D90E78B0>, 
'get_age': <function Person.get_age at 0x000001C4D9327940>, 
'_Person__growup': <function Person.__growup at 0x000001C4D9327310>, ...}  


### 5.3 私有成员总结
- 在python中，使用`_`单下划线或者`__`双下划线来标识一个成员被保护或者被私有化隐藏起来。但是不管使用什么
样的访问控制，都不能真正阻止用户修改类的成员。Python中没有绝对安全的保护成员或者私有成员。
- 因此，前导下划线只是一种警告或者提醒，需要遵守这个约定，不要**破坏封装**。
***

***概念：统一建模语言(Unified Modeling Language，UML)是一种为面向对象系统的产品进行说明、可视化
和编制文档的一种标准语言，是非专利的第三代建模和规约语言。UML是面向对象设计的建模工具，独立于任何具
体程序设计语言。***
