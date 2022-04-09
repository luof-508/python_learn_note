#!/usr/bin/env python3
# coding=utf-8
"""
@author: feng.luo
@time: 2022/4/7
@File: logger_analysis_3_dispatcher_info.py
生产者-消费者模型，以寄信为例： 生产者 -- 缓冲区 -- 消费者
    1、写信的人 -- 制造数据，生产者
    2、投递信到邮箱 -- 数据放入缓冲区
    3、邮递员把信拿到邮局分发到目的地 -- 处理数据，消费者
使用生产者-消费者模型好处：
    解耦：写信人和邮递员看似无关，如无邮箱，则有强耦合关系。写信的人必须认识邮递员，且必须在固定的时间、地点等候邮递员取信；如果邮递员请教请假或换人了，
        还需要重新认识邮递员。可见，通过邮箱的，解决了生产者和消费者的依赖关系。
    并发，提高效率：寄信要一直在邮递员取信的地点等，很费时间，还可能等不到。通过信箱，所有寄信的人写好信后直接往邮箱里投，不用等；邮递员也不用挨家挨户
        的上门取信，只需从邮箱一次拿走。可见，生产者-消费者模型可以极大提高效率。
    支持忙闲不均：遇到节假日信封、包裹较多，邮递员一次拿不走，还可以留在邮箱，下次再拿。可见，生产者-消费者模型还可以解决生产者、消费者能力不均衡的问题。

生产者-消费者模型三种关系：
    生产者与生产者 -- 互斥
    消费者与消费者 -- 互斥
    生产者与消费者 -- 同步与互斥
    互斥：线程锁的问题，保证线程安全。比如，某一时刻生产者1从缓冲区拿数据data1，其他生产者不能在这一时刻拿数据，避免产生重复、甚至错误结果。

* 广义的凡有上下级数据传输打过程，都可以称为生产者消费者模型。这种模型，速度很难做到统一，因此需要消息队列，起到缓冲作用。另外，生产者生产速度不稳定，
  有可能造成短时间数据的'潮涌'，需要缓冲；不同消费者能力也不一样，通过数据缓冲，可以差异化决定消费缓冲区中数据的速度。
* 水库有干涸期和蓄洪期，但是水库蓄洪也有能力的，所以消息队列也有上限。
* 消费者能力一般要大于生产者，略大于都不行，万一有一个消费者挂了呢。

单机可以使用内建模块queue，构建进程内的队列，满足多个线程间的生产、消费需求。大型系统，可以使用中间件，例如RabbitMQ、RocketMQ、kafka。

queue模块：提供一个先进先出的队列。
    q = queue.Queue(maxsize=0):创建FIFO队列，返回Queue对象。当maxsize<=0，队列长度没有限制
    q.get(block=True,timeout=None): 从队列中移除元素，并返回这个元素；
        block=True，为阻塞；block=False，未拿到数据直接抛empty异常，设置timeout无效。
        timeout=None，表示不设超时，未拿到数据一直阻塞；timeout=5，阻塞5秒，未拿到数据抛empty异常。
    q.put(item,block=True,timeout=None):把一个元素item加入到队列中去。
    还有q.get_nowait(),q.put_nowait(item)方法

"""
import datetime
import queue
import re
import threading
import traceback
from queue import Queue

from tool.logger_define import LoggerDefine


logger = LoggerDefine(__name__).get_logger
_log_test_strs = '123.125.71.36 - - [06/Apr/2017:18:09:25 +0800] "GET /o2o/media.html?menu=3 HTTP/1.1" 200 8642 "-" ' \
                 '"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"'
pattern = r'(?P<remote>[\d.]{7,}) - - \[(?P<datetime>[^\[\]]+)\] "(?P<request>[^"]+)" (?P<status>\d+) (?P<size>\d+) "-"' \
          ' "(?P<useragent>[^"]+)"'
regex = re.compile(pattern)
ops = {
    "datetime": lambda x: datetime.datetime.strptime(x, "%d/%b/%Y:%H:%M:%S %z"),
    "request": lambda x: dict(zip(('method', 'url', 'protocol'), x)),
    "status": int,
    "size": int
}


#####################################################################################
# 数据加载与提取
def extract_info(line: str):
    ret = regex.match(line)
    if ret:
        return dict((k, ops.get(k, lambda x: x)(v)) for k, v in ret.groupdict().items())


def load_info(path: str):
    with open(path, encoding='utf8') as f:
        for line in f:
            ret = extract_info(line)
            if ret:
                yield ret


src_info = load_info('test.log')


#####################################################################################
# 时间窗口函数
def window(src: Queue, handler, width: int, interval: int):
    start_time = datetime.datetime.strptime('1970/01/01 01:01:01 +0800', "%Y/%m/%d %H:%M:%S %z")
    delta = datetime.timedelta(seconds=width-interval)
    buffer = []
    while True:
        try:
            data = src.get(timeout=5)
        except queue.Empty:
            err_msg = traceback.format_exc()
            logger.error('Error: {}'.format(err_msg))
            return
        if not data:
            continue
        current = data['datetime']
        buffer.append(data)
        if (current - start_time).total_seconds() > interval:
            ret = handler(buffer)
            print(ret)
            buffer = [x for x in buffer if x['datetime'] > current - delta]
            start_time = current


def do_nothing_handler(iterable):
    print(iterable)
    return iterable


#####################################################################################
# 分发器
def dispatcher():
    """
    分发器（调度器）实现：数据加载load -- 数据提取extract -- 数据分发 |-- 消费者1数据分析window
                                                             |-- 消费者2数据分析window
                                                             |-- 消费者3数据分析window
    大量数据处理：通过分发器，将数据分发给多个消费者处理数据；每个消费者拿到后，通过同一个窗函数处理数据（不同的handler、width、interval）
    ，因此要有函数注册机制。
    如何分发：轮询，一对多的，多副本方式，把同一份数据分发给不同的消费者处理
    消息队列如何使用：数据载入后放入queue中，分发器从queue中拿数据，分发给不同的消费者。
    如何注册：调度器内部记录有哪些消费者，并记录消费者的自己的队列。
    多线程：每一个消费者一个线程。
    :return:
    """
    threads = []
    queues = []

    def _reg(handler, width, interval):
        # 注册函数：实例化一个线程对象，并保存；每一个线程各自有一个队列，保存自己要处理的数据
        src = Queue()
        queues.append(src)
        t = threading.Thread(target=window, args=(src, handler, width, interval))
        threads.append(t)

    def _run():
        # 数据分发；并调度函数，各自处理数据
        for t in threads:
            t.start()
        # 数据分发
        for data in src_info:
            for q in queues:
                q.put(data)
    return _reg, _run


reg, run = dispatcher()

# 注册窗口
reg(do_nothing_handler, 8, 5)

# 启动：数据分发并调度函数处理数据
run()
