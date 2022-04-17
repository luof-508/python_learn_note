#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/17
@File: install_operate.py
"""
from tool.logger_define import LoggerDefine

logger = LoggerDefine().get_logger


class InstallOperate:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def check_ip_accessible(ip):
        logger.info('check {} accessible'.format(ip))
        # todo python实现ping IP
        return True


if __name__ == '__main__':
    pass
