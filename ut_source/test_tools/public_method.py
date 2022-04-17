#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/17
@File: public_method.py
"""
import json


class PublicMethod:
    def __init__(self):
        pass

    @classmethod
    def get_json_file(cls, path):
        with open(path, encoding='utf8') as f:
            return json.load(f)


if __name__ == '__main__':
    pass
