# 模块化

一般来说，编程语言中，库、包、模块是同一种概念，是代码的组织方式。  
**python中只有一种模块对象类型<class 'module'>。但是为了模块化组织模块的便利，提供了包的概念。**  
**模块module**：指python的源代码文件。`.py`文件就是一个模块；**自定义模块名见名知意、全小写，开发环境中，自定义模块优先级最高，最先被搜索，不要和系统模块冲突**  
**包package**：指模块组织在一起的和包名同名的目录及其相关文件。通过`__init__.py`组织。  

## 一、导入语句
### 完全导入：`import name` 或`import ... as ...`   
**导入逻辑**：找到指定的模块名name，加载并初始化它，生成模块对象name。注意：这个对象，在import所在的作用域的局部命名空间中有效。例如，当再一个函数中导入，则这个模块对象name仅在函数作用域有效。  

**小结：** 导入顶级模块，其名称会加入到本地名词空间中，并绑定到其模块对象。导入非顶级模块，将其顶级模块加入到本地名词空间中，且必须使用完全限定名（从顶级模块开始的完整路径）来访问；如果使用了as，则使用as后的别名访问即可，且别名被加入到本地名词空间中。  

### 部分导入：`from ... import name (as...)`  
**导入逻辑**：找到from子句中指定的模块，加载并初始化（不导入）；import子句后的名称name被导入并保存到本地名称空间，name的搜索顺序是先查找from子句模块的属性，如果没有，再搜索子模块的，如果子模块也没有则抛出ImportError  
被导入的模块或模块内的指定资源name都是有边界的，这个name只是与导入时被加载和初始的模块资源的一个映射，导入的当前作用域名称空间保存这个name，是这个映射的标识符，可以通过这个标识符调用模块的资源。因此通过dir()时，只会打印出这个标识符，而不会列出被导入模块的其他属性。  

所有加载的模块都会记录在`sys.modules`中，`sys.modules`存储已经加载过的所有模块的字典  

## 二、模块的运行
`__name__`：每个块都有一个特殊属性`__name__`代表当前模块的名称，默认为源代码文件名；如果是包，则有限定名，例如`python_learn_note.chapter3_file_io`。可以在模块中显式的修改`__name__`，但是不要这么干。  

解释器初始化的时候：会初始化`sys.modules`（保存已加载的模块）-> 创建builtin模块（内建对象）-> `__main__`模块 -> sys模块，以及模块的搜索路径sys.path  

python是解释性脚本语言，任何一个脚本都可以从上到下一行行直接执行也可以作为模块被导入。  
**当模块作为主入口直接执行的时候，解释器会自动将`__name__`设置为`__main__`，则模块的顶层代码（模块中没有缩进的代码）就在`__main__`这个作用域中执行；如果是import导入的，其`__name__`默认就是模块名。**  
所以，可有通过`if __name__ == __main__`：语句，测试本模块的功能，及避免主模块变更的副作用：当主模块变为导入模块时，由于顶层代码没有封装，被import的时候一并执行了。  

## 三、模块的属性
|名称|含义|  
|:-:|:-|  
|`__name__`|模块名  
|`__file__`|字符串，源文件路径  
|`__package__`|当模块是包，同`__name__`  


## 四、包：package
**包，特殊的模块，类型都是`<class 'module'>`**  
创建一个目录，并在该目录下创建一个`__init__.py`文件，则这个目录就可以作为模块，这就是包，代码写在`__init__.py`中包目录下的py文件、子目录都是其子模块。python3没有`__init__.py`不影响导入，但是这不符合python编程规范。  

**示例：**  
**示例包结构：**  
>`module_test`  
 &ensp;&ensp;&ensp;&ensp;|-- `__init__.py`  
 &ensp;&ensp;&ensp;&ensp;|-- `foo.py`  
 &ensp;&ensp;&ensp;&ensp;|-- `module_test.py`  
 &ensp;&ensp;&ensp;&ensp;|-- `module_test1`  
      &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;|-- `__init__.py`  
      &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;|-- `module_test2.py`    
`module_test.py`  
`module_test1.py`  

顶级`__init__.py`文件：  
```python
# __all__ = ['module_test']

test = 123
```

`module_test.py` 文件：  
```python
__all__ = ['_x', '__y']


print('This is module_test module')

_x = '_x'
__y = '__y'
z = 'zzz'


class A:
    def show_module(self):
        print('{}.a={}'.format(self.__module__, self))
        print(self.__class__.__name__)


def imp_test():
    pass


a = A()
a.show_module()
```

`module_test.py` 文件：
````python
import sys

from python_learn_note import chapter3_file_io  # 导入包，包具有`__package__`属性，同`__name__`
import module_test.module_test as mod  # 导入模块
print('local module')
import module_test.module_test
import module_test.module_test as test123  # 可见，模块不会被重复导入，同一个作用域，同一个模块只会被导入一次。

print(mod.imp_test, id(mod.imp_test))


############################
def mod_test():
    import module_test.module_test as mod
    print(mod.imp_test, id(mod.imp_test))
    from module_test import module_test
    print(module_test.imp_test, id(module_test.imp_test))


mod_test()
# 三个imp_test的id都是一样。说明导入模块时，模块被加载并初始化到内存一次，当再次导入时，直接从内存中取，不会再次加载，以防挤爆内存空间。


############################
for p in sys.path:  # 模块的路径搜索顺序
    # 当加载一个模块的时候，需要从这些搜索路径中从前到后依次查找，不会搜索子目录，找不到就抛异常。路径可以为字典、zip文件、egg文件。
    # sys.path可以被修改，追加新的目录
    print(p)


if __name__ == '__main__':
    # 当模块作为主入口直接执行的时候，解释器会自动将`__name__`设置为`__main__`，则模块的顶层代码（模块中没有缩进的代码）就在`__main__`这个作用域中执行；
    # 如果是import导入的，其`__name__`默认就是模块名。
    print(__name__)
    print(module_test.__name__)
    print(chapter3_file_io.__package__, chapter3_file_io.__name__)  # 包具有`__package__`属性，同`__name__`
    # `__file__`：字符串，源文件路径
    print(__file__, module_test.__file__)
````


## **模块和包的总结：**
包能够更好的组织模块，尤其是大模块代码很多，可以拆分成很多子模块，便于使用某些功能就加载相应的子模块。  
包目录中`__init__.py`是在包第一次导入的时候就会执行，内容可以为空，也可以是用于该包初始化工作的代码，最好不要删除它（低版本不可删除）  
导入子模块一定会加载父模块，但是导入父模块一定不会导入子模块  
包目录之间只能使用.点号作为间隔符，表示模块及其子模块的层级关系  

模块也是封装，如同类、函数，不过它能够封装变量、类、函数。  
**模块就是命名空间，其内部的顶层标识符，都是它的属性，可以通过 `__dict__`或`dir(module)`查看。**  

**包也是模块，但模块不一定是包，包是特殊的模块，是一种组织方式，它包含`__path__`属性**  


**问题**
`from json import encoder`之后，`json.dump`函数用不了，为什么？`import json.encoder`之后呢？`json.dump`函数能用吗？  
**原因：**
- `from json import encoder`，json仅仅是被加载了，保存在内存中，但当前名词空间没有json，故`json.dump`函数用不了
- `import json.encoder`，json被加载后，json保存在当前名词空间中，故可以使用。当前名称空间的json只是内存中被加载的json模块的映射或引用。  


## 五、绝对导入和相对导入：
**绝对导入**：总是去模块搜索路径中找；  
**相对导入**：**只能在包使用，且只能用在`from...import...`语句中。**  
.表示当前目录内  
..表示上一级目录  
...表示上上级。  
不要在顶层模块中使用相对导入  
**使用相对导入的模块，不能直接运行。使用相对导入的模块就是为了内部互相的引用资源，不是为了直接运行的**  

## 六、访问控制：  
1、下划线开头的模块名，属于合法的标识符，可以正常导入  
2、模块内的下划线开头的标识符：使用`from...import *`，无法导入以下划线开头的属性，`from ... import _name, __name`方式都可以正常导入。也就是说，模块内没有私有变量，下划线开头的属性不会做特殊处理
3、包和子模块的导入：`from...import *`，只能导入`__init__.py`中给出的属性，如果要导入子模块，需要在`__init__.py`的`__all__`中给出  

**`from...import *`和`__all__`示例：**   

`module_test1.py`文件：
```python
import ut_source
import ut_source.test_tools

print(dir())
print(type(ut_source))
print(ut_source.test_tools)
print(dir(ut_source))
print(ut_source.__package__)

# from .exception_handle_01 import MyException  # 使用相对导入的模块，不能直接运行。使用相对导入的模块就是为了内部互相的引用资源，不是为了直接运行的
# from .. import ut_source as ut


# 测试`__all__`对`from...import *`的控制：在模块中定义`__all__`，则`from...import *`，只会import `__all__`中给出的属性；
# 在包中使用`from...import *`，如果`__init__.py`没有给出`__all__`,则只会导入`__init__.py`中的属性，子模块都不会导入；如果给出`__all__`，则只会导入`__all__`中的属性
from module_test import *
print(dir())
from module_test.module_test import *
print(dir())
from module_test.module_test import z
print(dir())
print(sorted(list(locals().keys())))
print(locals())  # dir()就是sorted(list(locals().keys()))
```

## 总结：  
### 一、使用 `from xyz import *` 导入  
1．如果模块没有 `__all__`,`from xyz import *`只导入非下划线开头的模块的变量。如果是包，子模块也不会导入，除非在`__all__`中设置，或 `__init__.py` 中使用相对导入  
2．如果模块有`__all__`，`from xyz import *`只导入`__all__`列表中指定的名称，哪怕这个名词是下划线开头的，或者是子模块  
3. `from xyz import *`方式导入，使用简单，但是其副作用是导入大量不需要使用的变量，甚至有可能造成名称的冲突。而`__all__`可以控制被导入模块在这种导入方式下能够提供的变量名称，就是为了阻止`from xyz import *`导入过多的模块变量，从而避免冲突。因此，编写模块时，应该尽量加入`__all__`  

### 二、`from module import name1, name2` 导入  
这种方式的导入是明确的，哪怕是导入子模块，或者导入下划线开头的名称程序员可以有控制的导入名称和其对应的对象  


## 模块变量的修改
模块对象是同一个，因此模块的变量也是同一个，对模块变量的修改会影响所有使用者。除非万不得已，或者明确知道自己在做什么，否则不要修改模块的变量。  
所以可以通过打补丁的方法，修改模块的变量、类、函数等内容，例如猴子补丁。  
