#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/17
@File: implement_Install_driver.py
"""
import pathlib
import re
from except_handle.except_module import UTException
from tool.logger_define import LoggerDefine
from tool.install_operate import InstallOperate
from utils.request_tools import Ssh

logger = LoggerDefine().get_logger


class InstallDriverInf:
    def __init__(self, args):
        self.args = args
        self.float_ip = self.args.get('float_ip')
        self.user = self.args.get('user')
        self.passwd = self.args.get('passwd')
        self.opr = InstallOperate(args)

    def procedure(self):
        client = None
        try:
            logger.info('start to install driver')
            self.check_driver_pkg()
            if not self.opr.check_ip_accessible(self.float_ip):
                err_msg = 'ip {} not reachable'.format(self.float_ip)
                logger.error(1, err_msg)
                raise UTException(1, err_msg)
            client = Ssh.creat_client(self.float_ip, self.user, self.passwd)
            if not client:
                err_msg = 'The connection request failed'
                logger.error(err_msg)
                raise UTException(1, err_msg)
            cmd = 'sh install_driver.sh; echo $?'
            ret = Ssh.send_command(client, cmd)
            logger.info('cmd ret:{}'.format(ret))
            if not re.search('success', ret):
                err_msg = 'Driver installation failure, details:{}'.format(ret)
                logger.error(err_msg)
                raise UTException(1, err_msg)
        except Exception as e:
            logger.error('ERROR:{}'.format(e))
            raise e
        finally:
            if client:
                Ssh.close_client(client)
        logger.info('Driver installation completed')
        return True

    def check_driver_pkg(self):
        pkg_path = self.args.get('driver_pkg_path')
        logger.info('check driver pkg:{}'.format(pkg_path))
        if not pathlib.Path('../', pkg_path).exists():
            err_msg = 'The {} does not exist'.format(pkg_path)
            logger.error(err_msg)
            raise UTException(1, err_msg)


if __name__ == '__main__':
    print(pathlib.Path('../', 'test_tools/driver_version1.0.zip').exists())
