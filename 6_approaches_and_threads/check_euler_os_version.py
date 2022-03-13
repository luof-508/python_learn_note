#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/3/12
@File: check_euler_os_version.py


多线程查询节点系统内核

需求分析：
1、多线性日志处理，收集处理子线程日志：
    a、日志文件要打印线程号，
    b、error日志搜集
    c、error日志和info日志分别处理

2、网路编程，如何建立客户端
3、多线程
4、统一处理、统一报错

"""
import logging

from python_learn_note.tool.logger_define import LoggerDefine


class LoggerDefineInf(LoggerDefine):
    def __init__(self):
        super().__init__()
        self.fn = logging.Formatter("[{asctime}-{name}]{process}-{thread}-{filename}-{level}:{message}", style='{')


logger = LoggerDefineInf().logger_define(file=__file__)


class SSHClientInf(object):
    def __init__(self):
        pass

    def create_ssh_client(self):
        pass

    def execute_command_return_result(self):
        pass


class EulerOSVersionCheckInf(object):
    def __init__(self):
        self.node_info = [
            {'manage_ip': '192.168.8.21', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.21', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.21', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.21', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.21', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
        ]

    def procedure(self):
        pass


if __name__ == '__main__':
    # os.path.splitext() 将文件名和扩展名分开
    # os.path.split() 返回文件的路径和文件名

    pass
