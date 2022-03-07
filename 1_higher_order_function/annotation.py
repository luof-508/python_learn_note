"""
参数注解、inspect模块、functools模块

一、python函数弊端：
    1、动态编译语言中的强类型语言，变量类型是在运行期决定的，因此不容易做类型检查，测试的时候可能不会测到，有的问题可能上线后才会暴露
    2、不知道函数传入的参数类型，使用者不知道函数设计，不知道传入什么类型的参数

二、解决方案：
    1、文档字符串，
    2、参数注解annotation(python3.5引入)，
      参数注解并不是限定，只是一种声明。给第三方工具做代码分析，发现隐藏bug，注解信息保存在属性__annotations__中

inspect模块：检查、审阅
inspect.signature: 按顺序拿到函数定义的 参数及其注解，返回一个有序字典


functools模块：
  1、partial:
"""
import inspect
import functools
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

fn = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
ch = logging.StreamHandler()
ch.setLevel(level=logging.INFO)
ch.setFormatter(fn)

logger.addHandler(ch)


def check_func_params(func_name):
    @functools.wraps(func_name)
    def _check_wrap(*args, **kwargs):
        sg = inspect.signature(func_name)
        params = sg.parameters
        logger.info('Function: {}, signature:{}'.format(func_name.__name__, params))
        # 检查位置参数
        values = list(params.values())
        for i, param in enumerate(args):
            if values[i].annotation is not values[i].empty and not isinstance(param, values[i].annotation):
                err_msg = 'Num:{}, param:{}, Parameter type do not match, signature type:{}, input type:{}'.format(
                    i+1, values[i].name, values[i].annotation, type(param))
                logger.error(err_msg)
                raise TypeError(err_msg)
        # 检查关键字参数
        logger.info('kwargs:{}'.format(kwargs))
        for k, v in kwargs.items():
            if params[k].annotation is not params[k].empty and not isinstance(v, params[k].annotation):
                err_msg = 'Param:{}, Parameter type do not match, signature type:{}, input type:{}'.format(
                    k, params[k].annotation, type(v))
                logger.error(err_msg)
                raise TypeError(err_msg)
        res = func_name(*args, **kwargs)
        logger.info('result:{}'.format(res))
        return res
    return _check_wrap


@check_func_params
def add(x: int, y: int = 7) -> int:
    """
    加法函数
    """
    # res = 0
    # for param in args:
    #     res += param
    # for _, v in kwargs.items():
    #     res += v
    return x + y


if __name__ == '__main__':
    # print(add.__annotations__)
    # print(add(1, 2), type(add(1, 2)))
    # print(add('1', '2'), type(add('1', '2')))
    # print(inspect.isfunction(add))
    sig = inspect.signature(add)
    logger.info('All signature:{}'.format(sig))
    # print(sig.parameters)
    # print(sig.parameters['x'].annotation)
    # print(sig.parameters['args'].annotation)
    # inspect.ismethod()
    # inspect.isgeneratorfunction()
    # inspect.isgenerator()
    # print(inspect.ismodule(inspect))
    # inspect.isbuiltin()
    # add('1', y='2')

    print(sorted({'1': 1, '2': 2}.items()))
