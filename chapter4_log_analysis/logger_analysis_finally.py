#!/usr/bin/env python3
# coding=utf-8
"""
@author: f.l
@time: 2022/4/9
@File: logger_analysis_finally.py
web server日志分析（status分析和useragent）流程：
    信息加载与提取：load函数和extract函数 -> 数据采集与处理：滑动窗口window函数和handler函数 ->
    最终落地需要采用生产者消费者模型，通过多线程实现数据分发、数据缓冲和函数调度，多任务高效处理不同分析信息的需求，dispatcher函数
"""
import collections
import datetime
import pathlib
import queue
import re
import threading
import traceback

import user_agents

from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger

_log_test_strs = '123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET /o2o/media.html?menu=3 HTTP/1.1" 200 8642 "-" ' \
                 '"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'
pattern = r'(?P<remote>[\d.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "-" "(?P<useragent>[^"]+)"'
regex = re.compile(pattern)
ops = {
    "datetime": lambda x: datetime.datetime.strptime(x, "%d/%b/%Y:%H:%M:%S %z"),
    "request": lambda x: {zip(('method', 'url', 'protocol'), x.split())},
    "status": int,
    "size": int,
    "useragent": lambda x: user_agents.parse(x)
}


# 数据提取和加载
def source_load(*paths):
    path_list = []
    for path in paths:
        p = pathlib.Path(path)
        if not p.exists():
            continue
        if p.is_file():
            path_list.append(p)
        elif p.is_dir():
            path_list.extend([pathlib.Path(f) for f in p.iterdir() if f.is_file() and not str(f).startswith('.')])
    for p in path_list:
        yield from open_file(p)


def open_file(path: pathlib.Path):
    with path.open(encoding='utf8') as f:
        for line in f:
            ret_dic = extract(line)
            if ret_dic:
                yield ret_dic
            else:
                # todo 抛异常或打印error日志，统计未解析成功的日志
                continue


def extract(line: str):
    ret = regex.match(line)
    if ret:
        return {k: ops.get(k, lambda x: x)(v) for k, v in ret.groupdict().items()}


# 数据采集和处理
def window(src: queue.Queue, handler, width: int, interval: int):
    """按宽度width采集数据，并将采集的数据穿个handler处理

    :param src: 加载的数据, 生成器
    :param handler: 数据处理函数
    :param width: 数据采集宽度
    :param interval: 数据采集间隔
    :return:
    """
    start_time = datetime.datetime.strptime('1970/01/01 01:01:01 +0800', "%Y/%m/%d %H:%M:%S %z")
    delta = datetime.timedelta(width - interval)
    buffer = []
    while True:
        try:
            data = src.get(timeout=2)
        except queue.Empty:
            err_msg = traceback.format_exc()
            logger.error('Error:{}'.format(err_msg))
            return
        if not data:
            continue
        current = data['datetime']
        buffer.append(data)
        if (current - start_time).total_seconds() > interval:
            ret = handler(buffer)
            # 打印结果
            print(ret)
            start_time = current
            buffer = [d for d in buffer if current - d['datetime'] < delta]


def status_handler(iterable):
    s = dict()
    for data in iterable:
        status = data['status']
        if not s.get(status):
            s[status] = 0
        s[status] += 1
    total = sum(s.values())
    return {k: float('{:.2f}'.format(v/total*100)) for k, v in s.items()}


browser_ret = collections.defaultdict(lambda: 0)


def browser_handler(iterable):
    for data in iterable:
        ua = data['useragent']
        browser_ret[ua.browser.family, ua.browser.version_string] += 1
    return browser_ret


# 数据分发和函数调度
def dispatcher():
    """
    函数注册：即为数据处理函数实例化一个线程和传入函数参数
    函数分发：起线程分析数据
    # 调度器需要记录每一个注册函数的队列，以便于为每一个函数（消费者）分发数据
    :return:
    """
    threads = []
    queues = []

    def _reg(handler, width, interval):
        q = queue.Queue()
        queues.append(q)
        t = threading.Thread(target=window, args=(q, handler, width, interval))
        threads.append(t)

    def _run():
        for t in threads:
            t.start()
        for data in loaded_src:
            for q in queues:
                q.put(data)
    return _reg, _run


if __name__ == '__main__':
    # 数据载入
    loaded_src = source_load('test.log')
    # 数据分发和函数调度
    reg, run = dispatcher()
    # 函数注册
    reg(status_handler, 10, 5)
    reg(browser_handler, 10, 10)
    # 函数调度
    run()
