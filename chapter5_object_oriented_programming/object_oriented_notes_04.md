## 十二、Mixin  

假设文档类Document是所有文档类的抽象基类。Word、Pdf是Document的子类。  
**需求：** 为Document的子类提供打印能力  
**分析：** 因为Document的子类都具有打印能力，因此printf方法定义在Document中比较合适，
这样属性只在Document的`__dict__`保留一份就可以了。基类提供的`printf`方法不应具体实现，
因为它未必适合子类的打印；子类Word、Pdf需要个性化，继承、重写就好了。  

**方案一、继承、重写：**  

```python
class Document:
    def __init__(self, content):
        self.content = content

    def printf(self):
        print(self.content)


class Word(Document):
    def printf(self):
        print('This content:{}'.format(self.content))

```
上述方案在以下场景又不太合适，比如：Word、Pdf类都继承自Document类，且都是属于第三方库，不允许重写；
又或者一个大型项目中有其他继承自Word类的子类，这些子类继承了Word类的printf方法。
这个时候通过继承、重写实现需求，则违反了开闭原则。**如何解决？**  

**方案二、继承后重写：PrintableWord(Word)**  
```python
class Document:  # 第三方库，不允许重新
    def __init__(self, content):
        self.content = content

    def printf(self):
        print(self.content)


class Word(Document):  # 第三方库，不允许重新
    def printf(self):
        print('This content:{}'.format(self.content))


class PrintableWord(Word):
    def printf(self):
        print('This is printable:{}'.format(self.content))

```

上述方案看似不错，但是对于一个类有非常多的子类，且这些子类通过要继承、重写实现不同的功能，上述方案会导致子类太多，非常繁琐。
>比如，Word子类应用网络中，应具备序列化功能，那子类中就应该实现序列化；但是序列化又有
> pickle、json、messagepack等，难道每种功能继承、重写一个子类吗？那又要实现序列化又要具备打印、甚至更多功能呢？
> 所以会产生太多的子类，过于繁琐。   

**如何解决？**  

**方案三、装饰类**
```python
class Document:  # 第三方库，不允许重新
    def __init__(self, content):
        self.content = content

    def printf(self):
        print(self.content)


class Word(Document):  # 第三方库，不允许重新
    def printf(self):
        print('This content:{}'.format(self.content))


def jsonable(cls):
    import json
    cls.jsonable = lambda self: json.dumps(self.content)
    return cls


@jsonable
class JsonableWord(Word):
    pass


if __name__ == '__main__':
    print(JsonableWord.__dict__)

```
**执行结果：**
>{'__module__': '__main__', '__doc__': None, 'jsonable': <function jsonable.<locals>.<lambda> at 0x00000170A5249AF0>}  

**小结：**
- 上述方案，是最传统、典型的类继承、设计流程。
- 用装饰器增强一个类，把功能给附加上去，哪个类需要就装饰它，动态添加、简单方便。

***对于复杂的项目，可能需要增强很多的功能，这个时候用装饰器可能就不太好了，怎么办？***  
**方案四、Mixin设计模式**  

**先看示例：**
```python
import pickle


# 通过Mixin，缺什么补什么，比如Pdf类，要实现实现网络传输，缺序列化功能
class Document:
    def __init__(self, content):
        self.content = content

    def printf(self):
        print(self.content)

class Pdf(Document):  # 第三方库，不允许重新
    pass


class SeriaPdfMixin:
    def serialization_content(self, content):
        return pickle.loads(content)


class SeriaPdf(SeriaPdfMixin, Pdf):
    pass


if __name__ == '__main__':
    print(SeriaPdf.__mro__)
    print(SeriaPdf.__dict__)
```
**执行结果：**
>(<class '__main__.SeriaPdf'>, <class '__main__.SeriaPdfMixin'>, <class '__main__.Pdf'>, <class '__main__.Document'>, <class 'object'>)  
{'__module__': '__main__', '__doc__': None}  

从执行结果可知，`SeriaPdf`类先从自己的类中找属性，然后从`SeriaPdfMixin`类中找，再从`Pdf`类中找，及C3算法的查找顺序。**`SeriaPdf`通过多继承，实现了增加序列化属性，且未破坏第三方库，同时还可以通过这种方式扩展更多功能，这就是Mixin。**

**如何理解Mixin？**
- Mixin,体现了一种更加流行、非常重要的设计模式--组合的设计模式。**缺什么补什么**。本质上是利用多继承，实现的一种叫做**组合的设计模式**；
继承也是一种设计模式，继承其实叫泛化。组合比继承更好，利用多继承，把需要增强的类放到多继承的列表里面去，多种不同功能的类混合在一起，实现更强大的功能。
- Mixin通过类的多继承，实现功能增强，比装饰器更加灵活。对于需要混进去的的功能非常多等复杂场景，用Mixin来做比用装饰器更清晰，更好，扁平扩展。
简单问题，装饰器两下搞定，复杂问题，用Mixin；二者都很高大上。

**组合与继承的对比**  
对于一个需求，组合的设计思想是：把每一个需要的功能写一个类来实现，然后将这些功能放在多继承列表的前面，组合过来，实现更强大的功能，缺什么补什么。
继承思想：在已经继承的基类上实现需要的所有功能，子类继承过来。但是需求、功能会是随着发展动态变化的，根本无法做到在基类上实现所有功能。例如：
>设计一个机器人：缺胳膊，加胳膊；缺腿加腿；缺轱辘加轱辘，通过组合实现。如果通过继承，那么上面的基类就需要非常丰富，能囊括机器人的所有抽象属性，
> 基类不丰富，则机器人类就要非常丰富；那如果以后要动态增加更多功能呢，现在的机器人只能走，但是保不齐以后机器人可以飞、可以潜水呢？ 
> 所以不要以固定思维设计未来这个类，类的功能都是动态变化的，不可能在设计之初就覆盖未来的所有功能。  
> **就用Mixin方式，组合。组合是优于继承的。能少继承，则少继承，其他方式用组合的方式来实现。**  

**Mixin使用原则**：  
1. Mixin类不应显示的出现`__init__`，为什么，你是混进去增强功能的，初始化干嘛，增强的东西相当于都是类属性，而不是增强实例的属性。  
2. Mixin类通常不能独立工作。为什么，就像机器人的例子，它只是一支腿、一个胳膊，是组合用的。  
3. Mixin类如果有继承发生，Mixin的祖先类应该也是Mixin类。

**注意：使用时，Mixin类通常在继承列表的第一个位置(C3算法，从最左边开始找)，例如**：  
`class PrintableWord(PrintableMixin, Word):pass`

**Mixin和装饰器，这两种方式都非常好，都是一种组合的设计模式，看个人喜好。**   

**推荐书籍**：有足够的实践后，看看UML

