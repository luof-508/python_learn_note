#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/5/10
@File: module_handle_02.py

五、绝对导入和相对导入：
绝对导入：总是去模块搜索路径中找；
相对导入：**只能在包使用，且只能用在`from...import...`语句中。**
.表示当前目录内
..表示上一级目录
...表示上上级。
不要在顶层模块中使用相对导入
**使用相对导入的模块，不能直接运行。使用相对导入的模块就是为了内部互相的引用资源，不是为了直接运行的**

六、访问控制：
1、下划线开头的模块名，属于合法的标识符，可以正常导入
2、模块内的标识符：使用`from...import *`，无法导入以下划线开头的属性，`from ... import _name, __name`方式都可以正常导入。也就是数，模块内没有私有变量，下划线开头的属性不会做特殊处理
3、`from...import *`和`__all__`：
4、包和子模块的导入：`from...import *`，只能导入`__init__.py`中给出的属性，如果要导入子模块，需要在`__init__.py`的`__all__`中给出

总结：
一、使用 `from xyz import *` 导入
1．如果模块没有 `__all__`,`from xyz import *`只导入非下划线开头的模块的变量。如果是包，子模块也不会导入，除非在`__all__`中设置，或 `__init__.py` 中使用相对导入
2．如果模块有`__all__`，`from xyz import *`只导入`__all__`列表中指定的名称，哪怕这个名词是下划线开头的，或者是子模块
3. `from xyz import *`方式导入，使用简单，但是其副作用是导入大量不需要使用的变量，甚至有可能造成名称的冲突。而`__all__`可以控制被导入模块在这种导入方式下能够提供的变量名称，就是为了阻止`from xyz import *`导入过多的模块变量，从而避免冲突。因此，编写模块时，应该尽量加入`__all__`

二、`from module import name1, name2` 导入
这种方式的导入是明确的，哪怕是导入子模块，或者导入下划线开头的名称程序员可以有控制的导入名称和其对应的对象


模块变量的修改：
模块对象是同一个，因此模块的变量也是同一个，对模块变量的修改会影响所有使用者。除非万不得已，或者明确知道自己在做什么，否则不要修改模块的变量。
所以可以通过打补丁的方法，修改模块的变量、类、函数等内容，例如猴子补丁。

"""
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

