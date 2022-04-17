#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/17
@File: set_path.py
"""
import sys
import mock
import unittest


sys.modules['utils.request_tools'] = mock.MagicMock()


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass


if __name__ == '__main__':
    pass
