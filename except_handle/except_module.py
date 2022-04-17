#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/17
@File: except_module.py
"""
from except_handle.err_code_module import ErrorCode


class UTException(BaseException):
    # TODO 设计异常处理模块
    def __init__(self, err_code, err_msg, *args, **kwargs):
        self.err_code = err_code
        self.err_msg = err_msg

    def get_code_msg(self):
        err_msg = ErrorCode.get_code_msg(self.err_code) % self.err_msg
        return err_msg


if __name__ == '__main__':
    pass
