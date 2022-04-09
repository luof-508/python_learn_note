#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/4/9
@File: dispatcher.py
实现命令分发器：注册函数到某个命令，用户输入命令时，路由到注册的函数，如果没有此命令，执行默认函数
注册reg：其实就是建立命令到函数的映射关系，并保存下来，同时传入函数参数
分发run：根据用户输入的key，调用对应映射的函数。
"""
from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger


################################################################################################
# 基本结构
def dispatcher_demo():
    # 注册函数
    regs = {}

    def _reg(key):
        regs[key] = foo1
        pass

    # 函数分发
    def _run():
        while True:
            name = input()
            regs.get(name) if regs.get(name) else _default()

    # 默认函数
    def _default():
        pass
    return _reg, _run


def foo1():
    pass


reg_demo, run_demo = dispatcher_demo()
reg_demo('python')
run_demo()


################################################################################################
# 使用装饰器实现函数注册。根据输入的key值，执行对应映射的函数，实现分发；重复注册，报错；未输入参数执行默认函数。
def dispatcher():
    command_dic = {}

    def register(name):
        def _register(func):
            if command_dic.get(name):
                logger.error('No double registration')
                return
            command_dic[name] = func

        return _register

    def default_func(param=None):
        logger.info('Unknown cmd, pass')

    def _dispatcher():
        while True:
            cmd = input('Enter the cmd>>>')
            if cmd == 'quit':
                return
            param = input('Input the parameter or just press the enter>>>')
            command_dic.get(cmd, default_func)(param) if param else command_dic.get(cmd, default_func)()
    return register, _dispatcher


reg, disp = dispatcher()


@reg('python')
def func_1(param=None):
    if param:
        logger.info(f'This is func_1, parameter:{param}')
    else:
        logger.info(f'This is func_1, no parameter')


@reg('fg_luo')
def func_2(param=None):
    if param:
        logger.info(f'This is func_1, parameter:{param}')
    else:
        logger.info(f'This is func_1, no parameter')


@reg('fg_luo')
def func_3(param=None):
    pass


if __name__ == '__main__':
    disp()

