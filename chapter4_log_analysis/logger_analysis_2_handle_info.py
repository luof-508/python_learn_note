#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/4/6
@File: logger_analysis_2_handle_info.py

数据载入：数据就是日志的一行行记录，载入数据就是文件IO的读取。将获取数据的方法封装成函数，实现数据载入

数据分析：很多数据，都是和时间相关的，按照时间顺序产生的，数据分析的时候，需要按照时间求值。所以一般采用时间窗分析

时间窗分析(滑动窗口)：
    interval：表示每一次求值的时间间隔
    width：时间宽度，指每一次求值的时间窗口宽度
    当width > interval时：数据求值会有重叠；否则数据会有丢失，一般不采用这种方案

时序数据：
    运维环境中，日志、监控等产生的数据都是与时间相关的数据，按照时间先后产生并记录下来的数据，所以一般按照时间对数据进行分析。

数据分析基本程序结构：载入数据（load函数） -- 提取数据（extract函数）-- 分析数据（（window窗函数获取数据，调用handler函数处理数据）


"""
import datetime

from tool.logger_define import LoggerDefine
from logger_analysis_1_extract_info import RegularExtract


logger = LoggerDefine(__name__).get_logger


class HandleInfo(RegularExtract):
    """
    数据分析基本程序结构：载入数据（load函数） -- 提取数据（extract窗函数）-- 处理数据（window + handler函数）
    """
    def __init__(self):
        super().__init__()

    def source_load(self, path):
        """载入数据"""
        with open(path, encoding='utf8') as f:
            for line in f:
                field = self.extract_info_by_regular_expression(line)
                if field:
                    yield field
                else:
                    continue  # TODO 解析失败处理：抛异常或打印error日志

    @staticmethod
    def window(src, handler, width, interval):
        """时间窗口函数

        :param src: 数据源，生成器，取数据
        :param handler: 数据处理函数
        :param width: 时间窗口宽度，秒
        :param interval: 处理时间间隔，秒
        """
        start = datetime.datetime.strptime("1970/01/01 01:01:01 +0800", "%Y/%m/%d %H:%M:%S %z")
        delta = datetime.timedelta(seconds=width-interval)
        buffer = []  # 窗口中待计算的数据
        for data in src:
            if not data:
                continue
            # 存入buffer中等待计算
            current = data['datetime']
            buffer.append(data)
            if (current - start).total_seconds() >= interval:
                ret = handler(buffer)
                # 打印结果
                print('ret:{}'.format(ret))
                start = current
                buffer = [x for x in buffer if x['datetime'] > current - delta]

    @staticmethod
    def handler_method(iterable):
        """
        数据处理函数
        """
        return iterable
        # vals = [x['value'] for x in iterable]
        # return sum(vals) // len(vals)


if __name__ == '__main__':
    hand = HandleInfo()
    hand.window(hand.source_load('test.log'), hand.handler_method, 8, 5)
