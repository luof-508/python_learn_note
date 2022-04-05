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
import datetime
import re
import threading
import time

from python_learn_note.tool.logger_define import LoggerDefine


logger = LoggerDefine(__file__).get_logger


class SSHClientInf(object):
    def __init__(self):
        pass

    @staticmethod
    def create_ssh_client(*args):
        return 'client'

    @staticmethod
    def execute_command_return_result(client):
        return 'eulerosv2r10'

    @staticmethod
    def close_client(client):
        pass


class EulerOSVersionCheckInf(object):
    def __init__(self):
        self.node_info = [
            {'manage_ip': '192.168.8.21', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.22', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.23', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.24', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
            {'manage_ip': '192.168.8.25', 'user_name': 'user', 'pwd': 'abc123', 'root_pwd': 'abc123'},
        ]
        self.ssh = SSHClientInf()
        self.res = {'kernel_err': [], 'ssh_err': [], 'timeout_err': []}

    def procedure(self):
        self.parallel_run(self._check_euler_os, self.node_info)
        result = []
        if self.res['kernel_err']:
            err_msg = 'kernel error node:{}'.format(self.res['kernel_err'])
            logger.error(err_msg)
            result.append(err_msg)
        if self.res['ssh_err']:
            err_msg = 'Ssh error node:{}'.format(self.res['ssh_err'])
            logger.error(err_msg)
            result.append(err_msg)
        if self.res['timeout_err']:
            err_msg = 'Timeout error node:{}'.format(self.res['timeout_err'])
            logger.error(err_msg)
            result.append(err_msg)
        if result:
            res = '\n'.join(result)
            raise Exception(res)

    def parallel_run(self, func, node_dic: list, para_num=3):
        para_dic = dict()
        for node in node_dic:
            logger.info('Start a new thread for node:{}'.format(node.get('manage_ip')))
            t = threading.Thread(target=func, args=(node,), daemon=True)
            para_dic[node.get('manage_ip')] = t, datetime.datetime.now()
            t.start()
            while threading.active_count() == para_num:
                logger.info('alive thread:{}'.format(threading.enumerate()))
                time.sleep(1)
        while para_dic:
            logger.info('check timeout thread:{}'.format(threading.enumerate()))
            self._check_thread(para_dic)
            time.sleep(1)

    def _check_thread(self, thread_dic: dict, timeout=15):
        check_dict = thread_dic.copy()
        for cur_ip, (cur_t, cur_time_stamp) in check_dict.items():
            if (datetime.datetime.now() - cur_time_stamp).total_seconds() > timeout:
                self.res['timeout_err'].append(cur_ip)
                thread_dic.pop(cur_ip)

    def _check_euler_os(self, *args):
        node_info = args[0]
        node_ip = node_info.get('manage_ip')
        user = node_info.get('user_name')
        pwd = node_info.get('pwd')
        root_pwd = node_info.get('root_pwd')
        time.sleep(1)
        try:
            client = self.ssh.create_ssh_client(node_ip, user, pwd, root_pwd)
        except Exception as e:
            logger.error('SSH Failed, details:{}'.format(e))
            self.res['ssh_err'].append(node_ip)
            raise Exception(e)
        try:
            res = self.ssh.execute_command_return_result(client)
        except Exception as e:
            logger.error('Execute cmd error, details:{}'.format(e))
            self.res['ssh_err'].append(node_ip)
            raise Exception(e)
        finally:
            self.ssh.close_client(client)
        if not re.search('eulerosv2r9', str(res)):
            logger.error('Kernel error, details:{}'.format(res))
            self.res['kernel_err'].append(node_ip)
        self.ssh.close_client(client)


if __name__ == '__main__':
    # os.path.splitext() 将文件名和扩展名分开
    # os.path.split() 返回文件的路径和文件名
    try:
        EulerOSVersionCheckInf().procedure()
    except Exception as e:
        logger.error('ERROR:{}'.format(e))
