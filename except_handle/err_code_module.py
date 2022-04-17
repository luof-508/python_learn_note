#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/17
@File: err_code_module.py
"""
from tool.logger_define import LoggerDefine


logger = LoggerDefine().get_logger


class ErrorCode:
    def __init__(self):
        pass

    @classmethod
    def get_code_msg(cls, code):
        # todo 设计从配置文件读取error code方法
        logger.info('get error code info:{}'.format(code))
        return UTErrorCode.UT_ERROR


class UTErrorCode:
    UT_ERROR = 'UT error, details: {}'


if __name__ == '__main__':
    pass
