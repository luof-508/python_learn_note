#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/9
@File: logger_analysis_5_web_analysis.py
日志分析最终流程：
数据源处理 -- 数据采集、分发、调度 -- 数据分析

浏览器分析：useragent
useragent：指的是软件（浏览器）安装一定的格式向远端的服务器提供一个标识自己的字符串。
useragent: 客户端信息，包含用户类型、什么操作系统、浏览器类型（IE、chrome）、浏览器版本、浏览器核心、spider等信息
http协议中，在http头传送user-agent字段。

user-agent可以随意修改。

chrome查看useragent：F12进入控制台--Console--navigator.userAgent

chrome useragent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
edge useragent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36'

分析useragent，可以查看大部分用户浏览器版本，然后可以做对应的版本兼容适配，满足大部分用户需求
浏览器browser分析和状态码status分析的差异在于：
    status分析，关注的是某一段时间内，状态码所占的比例，进而分析网站的效率、网站状态、是否有嗅探等。
    browser分析，关注很长一段时间内，用户所使用的浏览器是什么，进而做兼容适配，提升用户体验，指导测试侧重点。
    因此，status分析width、interval可能需要时间重叠，数据分析也是按interval进行；browser分析则不需要时间重叠，切统计了从开始到最后的总体数据

信息提取：
pyyaml、ua-parser、user-agents模块
"""
import collections
import datetime
from user_agents import parse

from logger_analysis_4_analysis_info import AnalysisInfo


class WebAnalysis(AnalysisInfo):
    def __init__(self):
        super(WebAnalysis, self).__init__()
        self.ops = {
            'datetime': lambda time_str: datetime.datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z"),
            'request': lambda request_str: dict(zip(('method', 'url', 'protocol'), request_str.split())),
            'status': int,
            'size': int,
            'useragent': lambda us: parse(us)
        }
        self.ua_dict = collections.defaultdict(lambda: 0)

    def browser_handler(self, iterable):
        for data in iterable:
            ua = data['useragent']
            self.ua_dict[ua.browser.family, ua.browser.version_string] += 1
        return self.ua_dict


if __name__ == '__main__':
    log_analysis = WebAnalysis()
    # 数据分发与函数调度
    reg, run = log_analysis.dispatcher()
    # 注册函数
    reg(log_analysis.status_handler, 10, 5)
    reg(log_analysis.browser_handler, 10, 10)
    # 函数调度
    run()
