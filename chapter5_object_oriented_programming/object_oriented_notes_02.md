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
- **私有属性，** 本质是类定义的时候，如果声明一个实例变量的时候，使用双下划线，python解释器会将其改名，转换为`_类__变量名`的名称。
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

***涉及概念：统一建模语言(Unified Modeling Language，UML)是一种为面向对象系统的产品进行说明、可视化
和编制文档的一种标准语言，是非专利的第三代建模和规约语言。UML是面向对象设计的建模工具，独立于任何具
体程序设计语言。***

## 6 补丁
**通俗理解打补丁：** 项目开发中，发现其中有几个类缺东西、缺功能，不补充可能影响业务，但是项目已经到了
发布必测阶段，这个时候大规模修改源码上CCB评审很麻烦，还要重新出包转测、重新发布很麻烦。怎么办？
>缺的东西、缺的功能写到一个临时文件中，临时增加，下次发布版本的时候再打包进去。这个临时文件的基本功能，
就是找到对应要增加、修改功能的类，然后修改或替换属性。  

**打补丁：** 修改或替换类的成员（属性）。使用者调用的方式没有改变，但是类提供的功能可能已经改变了。

**打补丁属于事后发现，是一种临时措施。**

```python
"""猴子补丁"""


class Person:
    def __init__(self, chinese, english, history):
        self.chinese = chinese
        self.english = english
        self.history = history

    def get_store(self):
        return self.chinese, self.english, self.history


def get_store(self):
    return dict(chi=self.__chinese, eng=self._english, his=self.__history)


def monkey_patch_person():
    Person.get_store = get_store  # 打补丁,要么在对象的属性上替换，要么在类的属性上替换


if __name__ == '__main__':
    stu1 = Person(97, 98, 99)
    print(stu1.get_store())
    monkey_patch_person()
    stu = Person(97, 98, 99)
    print(stu.get_store())
```
**猴子补丁：** monkey patch。 在运行时，对属性进行动态替换。就是把类添加、修改属性的过程，
封装到某个函数、某个类、某个模块里。要么在对象的属性上替换，要么在类的属性上替换。  

***这种外部修改，破坏了封装，临时用用就行了***

## 7 属性装饰器：@property  
**作用：** 把实例的属性保护起来，不让外部直接访问，外部使用getter方法读取属性，setter方法设置属性  

**三种方式实现getter、setter方法:**
```python
class Person:
    """三种方式实现getter、setter方法

    为了保护对象属性，不破坏封装，通常在设计的时候，提供属性的访问方法(读取、修改)：getattr, setattr
    """
    def __init__(self, chinese, english, history):
        self.__chi = chinese
        self._eng = english
        self.__his = history

    def get_chi(self):
        print('get chi')
        return self.__chi

    def set_chi(self, val):
        print('set chi={}'.format(val))
        self.__chi = val

    def del_chi(self):
        print('delete chi')
        del self.__chi

    @property
    def eng(self):
        print('get eng')
        return self._eng

    @eng.setter
    def eng(self, val):
        print('set eng={}'.format(val))
        self._eng = val

    @eng.deleter
    def eng(self):
        print('delete eng')
        del self._eng

    def set_his(self, val):
        print('set his={}'.format(val))
        self.__his = val

    def del_his(self):
        print('delete his')
        del self.__his

    his = property(lambda self: self.__his, set_his, del_his, 'this is his property')


if __name__ == '__main__':
    stu = Person(97, 98, 99)
    # 方式一，函数方法设置属性访问控制
    print(stu.get_chi())
    stu.set_chi(70)
    print(stu.__dict__)
    stu.del_chi()
    print(stu.__dict__)
    print('*' * 20)
    # 方式二，@property装饰器方式访问控制
    print(stu.eng)
    stu.eng = 60
    print(stu.__dict__)
    del stu.eng
    print(stu.__dict__)
    print('*' * 20)
    # 方式三、property类实例方式访问控制，应用较多
    print(stu.his)
    stu.his = 9
    print(stu.__dict__)
    del stu.his
    print(stu.__dict__)
```

## 8 对象销毁
有对象的初始化，就有对象的销毁。在类中可以定义`__del__`方法实现对象销毁。意义：  
- 初始化，有可能包含其他对象，比如链接网络、连接数据库，这些对象创建后，当当前实例要消亡的时候，需要关闭创建的这些对象（收尾工作）。  
- 在对象中定义`__del__`，在对象消亡前自动掉`__del__`方法，就可以完成上述收尾。
- python的垃圾回收不知道什么执行，所以一些场景在类中定义`__del__`方法是有必要的。  

## 9 方法重载（overload）  
- 其他面向对象的高级语言中才有重载的概念。所谓重载，就是同一个方法名，但是参数数量、类型不一样。就是同一个方法的重载。 
- python没有重载，也不需要重载，python方法定义中，形参非常灵活，不需要指定类型，送进去是什么类型就是什么类型，参数个数也不固定。
- python在继承中有**重写override**，重写一个方法。
- 重载是面向对象的一种方式，解决多态问题。

**函数级多态：** 一个函数解决了多种参数类型，或返回多种类型
