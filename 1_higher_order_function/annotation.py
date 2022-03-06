"""
python函数弊端：
    1、动态编译语言中的强类型语言，变量类型是在运行期决定的，因此不容易做类型检查，测试的时候可能不会测到，有的问题可能上线后才会暴露
    2、不知道函数传入的参数类型，使用者不知道函数设计，不知道传入什么类型的参数

解决方案：
    1、文档字符串，
    2、参数注解annotation(python3.5引入)，
      参数注解并不是限定，只是一种声明。给第三方工具做代码分析，发现隐藏bug，注解信息保存在属性__annotations__中

inspect模块：检查、审阅
inspect.signature: 按顺序拿到函数定义的 参数及其注解，返回一个有序字典

"""
import inspect


def add(x: int, y: int, *args, **kwargs) -> int:
    """
    加法函数
    :param x: int
    :param y:int
    :return: int
    """
    return x + y


if __name__ == '__main__':
    print(add.__annotations__)
    print(add(1, 2), type(add(1, 2)))
    print(add('1', '2'), type(add('1', '2')))
    print(inspect.isfunction(add))
    sig = inspect.signature(add)
    print(sig)
    print(sig.parameters)
    print(sig.parameters['x'].annotation)
    print(sig.parameters['args'].annotation)
    # inspect.ismethod()
    # inspect.isgeneratorfunction()
    # inspect.isgenerator()
    print(inspect.ismodule(inspect))
    # inspect.isbuiltin()
