#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/15
@File: test_case_01.py
"""
import sys
import mock
import pathlib
from ut_source.test_tools.set_path import MyTestCase
from ut_source.test_tools.public_method import PublicMethod
from ut_source.test_object.implement_Install_driver import InstallDriverInf


SSH = sys.modules['utils.request_tools'].Ssh


class TestInstallDriverInf(MyTestCase):
    def setUp(self) -> None:
        self.arg = PublicMethod.get_json_file(pathlib.Path('../').resolve()/'test_tools'/'fs_args.json')

    @mock.patch.object(SSH, 'send_command')
    @mock.patch.object(SSH, 'creat_client')
    def test_install_driver(self, mock_creat_client, mock_send_command):
        mock_creat_client.return_value = 'client'
        mock_send_command.return_value = 'success'
        # 非装饰器方式mock对象属性
        # SSH.creat_client = mock.Mock(return_value='client')
        # SSH.send_command = mock.Mock(return_value='success')
        # mock_check_pkg = InstallDriverInf.check_driver_pkg = mock.Mock(return_value='None')
        install_driver = InstallDriverInf(self.arg)
        install_driver.check_driver_pkg = mock.Mock(return_value=None)
        install_driver.opr.check_ip_accessible = mock.Mock(return_value=True)
        res = install_driver.procedure()
        SSH.creat_client.assert_called()
        SSH.send_command.assert_called()
        install_driver.check_driver_pkg.assert_called()

        self.assertEqual(True, res)


if __name__ == '__main__':
    ret = pathlib.Path('../').resolve()/'test_tools'/'fs_args.json'
    print(ret, type(ret))
