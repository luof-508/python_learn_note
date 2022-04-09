#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/9
@File: logger_analysis_4_analysis_info.py

完成日志分析功能：
    分析日志很重要，通过海量数据分析就能够知道是否遭受了攻击，是否被爬取及爬取高峰期，是否有盗链等。
    爬虫特点和浏览特点不一样，爬虫速度特别快，做html分析，分析是否为本站链接、跟进等。
    爬虫：su + http
百度爬虫名称：Baiduspider
谷歌爬虫名称：Googlebot

"""
import pathlib

from tool.logger_define import LoggerDefine
from logger_analysis_3_dispatcher_info import DispatcherInfo


logger = LoggerDefine(__name__).get_logger


class AnalysisInfo(DispatcherInfo):
    def __init__(self):
        super(AnalysisInfo, self).__init__()
        self.src_info = self.load_info('test.log')

    def load_info(self, *paths):
        """数据加载

        接收一批路径加载，判断路径是否存在。如果路径为普通文件，则当日志处理；如果为目录，则迭代目录下的普通文件，不深层次递归。
        """
        file_lst = []
        for path in paths:
            p = pathlib.Path(path)
            if not p.exists():
                continue
            if p.is_dir():
                file_lst.extend([f for f in p.iterdir() if f.is_file() and not str(f).startswith('.')])
            elif p.is_file():
                file_lst.append(p)
        for p in file_lst:
            yield from self.open_file(p)

    def open_file(self, path: pathlib.Path):
        with path.open(encoding='utf8') as f:
            for line in f:
                ret = self.extract_info_by_regular_expression(line)
                if ret:
                    yield ret
                else:
                    # TODO 未解析到信息抛出或打印日志
                    continue

    @staticmethod
    def status_handler(iterable):
        """状态分析

        状态码中包含了很多信息：比如：
        304，服务器收到客户端提交的请求参数，发现资源未变化，要求浏览器使用静态资源的缓存。304占比较大，说明静态缓存效果明显，服务器压力较小。
        404，服务器找不到请求的资源。404占比较大，说明html中出现了错误链接，或者尝试嗅探网站资源。
        如果400、500占比突然开始增大，网站肯定出现了问题。
        """
        ret = {}
        total = len(iterable)
        for data in iterable:
            status = data['status']
            if not ret.get(status):
                ret[status] = 0
            ret[status] += 1
        return {k: float('{:.2f}'.format(v/total*100)) for k, v in ret.items()}


if __name__ == '__main__':
    analysis_info = AnalysisInfo()
    # 数据分发与函数调度
    reg, run = analysis_info.dispatcher()
    # 注册窗口
    reg(analysis_info.status_handler, 8, 5)
    # 启动：数据分发并调度函数处理数据
    run()
